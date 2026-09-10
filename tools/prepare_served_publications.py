#!/usr/bin/env python3
"""Retrieve expected bytes from successful, source-bound Pages publications.

The post-merge proof must compare the deployed build, not manufacture a second
build with today's builder. Review artifacts and deploy jobs belong to the same
workflow run. A missing/expired artifact or an uncompleted exact-source deploy
is INCONCLUSIVE, never permission to use a different source revision.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

API = 'https://api.github.com'
REPOS = {'site': 'MattRoper1977/mattroper1977.github.io',
         'lessons': 'MattRoper1977/Lessons', 'apps': 'MattRoper1977/Matt-s-Apps-',
         'games': 'MattRoper1977/Games'}
WORKFLOWS = {'site': 'education-publication.yml', 'lessons': 'education-pages.yml',
             'apps': 'education-pages.yml', 'games': 'play-domain-publication.yml'}
ARTIFACTS = {'site': 'education-site-review', 'lessons': 'education-lessons-review',
             'apps': 'education-apps-review', 'games': 'standalone-games-review'}
UPLOAD_STEPS = {'site': 'Save the reviewed education output',
                'lessons': 'Save the reviewed education output',
                'apps': 'Save the reviewed education output',
                'games': 'Run actions/upload-artifact@v4'}


class Red(Exception):
    """A contradiction the tool OBSERVED. The evidence was reached and it
    disagrees: a digest that does not match, a publication that failed, an
    archive member that is a symlink, a caller misconfigured against this
    tool's own bounds. Exit 1."""


class Inconclusive(Exception):
    """The evidence could NOT BE REACHED. Nothing is claimed about the estate --
    the tool ran out of time or the network refused. Exit 2.

    GW1-C §1.2. These were one class until now: require() raised Inconclusive, so
    "the downloaded artifact digest differs" -- a real, observed defect -- reported
    in the same words and the same exit code as "I arrived before the publication
    finished". One channel carrying two opposite meanings, which is how twelve
    reds on main all read as a broken estate when they meant "I arrived early".

    NEITHER IS GREEN, and that is deliberate. A serve proof that could not measure
    must not read as proof; a wait that times out and returns green is the same
    defect in different clothes. The distinction is in what the run SAYS, not in
    whether it blocks."""


def require(ok, detail):
    """A contradiction. See Red."""
    if not ok:
        raise Red(detail)


def no_result(detail):
    """Evidence out of reach. See Inconclusive."""
    raise Inconclusive(detail)


def head(root):
    result = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    require(re.fullmatch('[a-f0-9]{40}', result), 'Invalid source revision')
    return result


def digest(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


class GitHub:
    def __init__(self, deadline):
        self.deadline = deadline
        self.started = time.monotonic()

    def waited(self):
        return int(time.monotonic() - self.started)
        self.token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
        require(self.token, 'Artifact provenance needs GITHUB_TOKEN with actions:read')

    def read(self, route, raw=False):
        if time.monotonic() >= self.deadline:
            no_result('no result: publication retrieval deadline reached, '
                      'waited %d seconds' % self.waited())
        url = API + route
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'mbm-served-publication',
                   'Authorization': 'Bearer ' + self.token, 'X-GitHub-Api-Version': '2022-11-28'}
        # urllib strips Authorization from cross-origin artifact redirects only
        # through this explicit handler, rather than forwarding the repository
        # token to the signed artifact storage URL.
        class ArtifactRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, request, fp, code, msg, response_headers, newurl):
                require(urllib.parse.urlsplit(newurl).scheme == 'https', 'Artifact redirect downgraded HTTPS')
                result = super().redirect_request(request, fp, code, msg, response_headers, newurl)
                if result is not None and urllib.parse.urlsplit(newurl).netloc != urllib.parse.urlsplit(request.full_url).netloc:
                    result.remove_header('Authorization')
                return result
        opener = urllib.request.build_opener(ArtifactRedirect())
        timeout = max(1, min(35, self.deadline - time.monotonic()))
        try:
            with opener.open(urllib.request.Request(url, headers=headers), timeout=timeout) as response:
                chunks = []
                size = 0
                while True:
                    if time.monotonic() >= self.deadline:
                        no_result('no result: publication download deadline reached, '
                                  'waited %d seconds' % self.waited())
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    require(size <= 1_000_000_000, 'Publication download is unexpectedly large')
                    chunks.append(chunk)
                data = b''.join(chunks)
        except (urllib.error.URLError, TimeoutError) as exc:
            raise Inconclusive(f'GitHub {route}: {exc}') from exc
        return data if raw else json.loads(data)


def publication_run_matches(kind, run, wanted, github):
    if run.get('head_branch') != 'main' or run.get('event') not in {'push', 'workflow_dispatch'}:
        return False
    if run.get('head_sha') == wanted:
        return True
    if kind != 'games':
        return False
    # Games intentionally deploys only when its publication inputs change.
    # A later engine-only main commit does not demand a new frozen publication.
    # Require all three triggering inputs to be byte-identical to current main;
    # never accept merely the newest green run or a coincidentally equal count.
    for file in ['games.json', 'play-publication.json', '.github/workflows/play-domain-publication.yml']:
        base = '/repos/' + REPOS[kind] + '/contents/' + file + '?ref='
        old = github.read(base + run['head_sha'])
        new = github.read(base + wanted)
        require(re.fullmatch('[a-f0-9]{40}', old.get('sha') or '') and
                re.fullmatch('[a-f0-9]{40}', new.get('sha') or ''),
                f'Games publication input {file} has no immutable blob identity')
        if old['sha'] != new['sha']:
            return False
    return True


def validate_artifact(artifact, run, kind):
    require(artifact.get('name') == ARTIFACTS[kind], 'Unexpected review artifact name')
    require(not artifact.get('expired'), f'{kind}: publication artifact expired')
    binding = artifact.get('workflow_run') or {}
    require(binding.get('id') == run['id'] and binding.get('head_sha') == run['head_sha'],
            f'{kind}: artifact does not bind to the successful publication source/run')
    require(re.fullmatch(r'sha256:[0-9a-f]{64}', artifact.get('digest') or ''),
            f'{kind}: GitHub did not supply an archive digest')


def timestamp(value):
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        require(parsed.tzinfo is not None, 'Publication timestamp lacks a timezone')
        return parsed
    except (AttributeError, TypeError, ValueError) as exc:
        raise Inconclusive(f'Invalid publication timestamp: {value!r}') from exc


def select_artifact(artifacts, run, jobs, kind):
    """A run ID survives reruns; bind the review to this successful attempt.

    Apps' activation took four attempts, each retaining a same-named review.
    Neither the first match nor merely the newest artifact proves which bytes
    were deployed. The successful attempt's actual upload step supplies the
    creation window, and its deploy job must be from that same attempt.
    """
    attempt = run.get('run_attempt')
    require(isinstance(attempt, int) and attempt > 0, f'{kind}: publication attempt missing')
    deploys = [job for job in jobs if re.search(r'(^| / )deploy$', job.get('name', ''))
               and job.get('run_attempt') == attempt and job.get('conclusion') == 'success']
    require(len(deploys) == 1, f'{kind}: successful deploy is not bound to this attempt')
    windows = [(job, step) for job in jobs if job.get('run_attempt') == attempt
               and job.get('conclusion') == 'success' for step in job.get('steps', [])
               if step.get('name') == UPLOAD_STEPS[kind] and step.get('conclusion') == 'success']
    require(len(windows) == 1, f'{kind}: expected one successful review upload in attempt {attempt}')
    job, step = windows[0]
    start, end = timestamp(step.get('started_at')), timestamp(step.get('completed_at'))
    require(start <= end <= timestamp(deploys[0].get('started_at')),
            f'{kind}: review upload does not precede this deployment')
    matches = [artifact for artifact in artifacts if artifact.get('name') == ARTIFACTS[kind]
               and start <= timestamp(artifact.get('created_at')) <= end]
    require(len(matches) == 1,
            f'{kind}: expected one review artifact within attempt {attempt} upload window, found {len(matches)}')
    artifact = matches[0]
    validate_artifact(artifact, run, kind)
    return artifact, {'run_attempt': attempt, 'upload_job_id': job['id'],
                      'deploy_job_id': deploys[0]['id'], 'upload_started_at': step['started_at'],
                      'upload_completed_at': step['completed_at']}


def extract_archive(data, destination):
    require(not destination.exists(), f'Refusing to overwrite publication directory {destination}')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = set()
        total = 0
        for item in archive.infolist():
            name = item.filename
            p = Path(name)
            require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,
                    f'Unsafe publication archive member: {name}')
            require(name not in names, f'Duplicate archive member: {name}')
            require(not stat.S_ISLNK(item.external_attr >> 16), f'Archive symlink: {name}')
            names.add(name)
            total += item.file_size
        require(names and total <= 2_000_000_000, 'Empty or oversized publication archive')
        destination.mkdir(parents=True)
        archive.extractall(destination)


def prepare_one(kind, wanted, output, github):
    repo = REPOS[kind]
    workflow = urllib.parse.quote(WORKFLOWS[kind], safe='')
    while time.monotonic() < github.deadline:
        runs = github.read(f'/repos/{repo}/actions/workflows/{workflow}/runs?branch=main&per_page=30')['workflow_runs']
        selected = None
        for run in runs:
            if not publication_run_matches(kind, run, wanted, github):
                continue
            if run.get('status') != 'completed':
                print(f'WAIT {kind}: publication {run["id"]} is {run.get("status")}', flush=True)
                break
            require(run.get('conclusion') == 'success', f'{kind}: exact-source publication {run["id"]} failed ({run.get("conclusion")})')
            jobs = github.read(f'/repos/{repo}/actions/runs/{run["id"]}/jobs?per_page=100')['jobs']
            deployments = [j for j in jobs if re.search(r'(^| / )deploy$', j.get('name', ''))]
            require(len(deployments) == 1 and deployments[0].get('conclusion') == 'success',
                    f'{kind}: successful deploy job missing; a saved review alone is not publication')
            selected = run
            break
        if selected is None:
            print(f'WAIT {kind}: no completed publication for source {wanted}', flush=True)
            time.sleep(min(10, max(0, github.deadline-time.monotonic())))
            continue
        artifacts = github.read(f'/repos/{repo}/actions/runs/{selected["id"]}/artifacts?per_page=100')['artifacts']
        artifact, attempt_evidence = select_artifact(artifacts, selected, jobs, kind)
        print(f'FETCH {kind}: source {selected["head_sha"]}, deployment {selected["id"]}, artifact {artifact["id"]}', flush=True)
        data = github.read(f'/repos/{repo}/actions/artifacts/{artifact["id"]}/zip', raw=True)
        require(digest(data) == artifact['digest'], f'{kind}: downloaded artifact digest differs')
        root = output / kind
        extract_archive(data, root)
        return {'root': str(root.resolve()), 'source_sha': wanted, 'publication_sha': selected['head_sha'],
                'run_id': selected['id'], 'run_url': selected['html_url'], 'artifact_id': artifact['id'],
                'artifact_sha256': artifact['digest'], 'deployment': 'success', **attempt_evidence}
    # GW1-C §1.2: name the seconds. "did not become available" is a fact about
    # the tool's patience, and a reader cannot tell whether it waited 4 seconds
    # or 40 minutes without being told which.
    raise Inconclusive(f'no result: {kind} exact-source publication did not become '
                       f'available, waited {github.waited()} seconds')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['site', 'lessons', 'apps', 'shelf', 'output']:
        parser.add_argument('--' + key, type=Path, required=True)
    # THREE NUMBERS THAT HAVE TO AGREE, and they are listed here because getting
    # two of them right is what shipped the last red:
    #
    #   1. this default and ceiling      -- how long the tool may wait
    #   2. the caller's --wait-seconds   -- .github/workflows/fieldops-p2-and-sweep.yml
    #   3. that job's timeout-minutes    -- must exceed (2), or the job is killed
    #                                       mid-wait and the wait buys nothing
    #
    # The wait is for the Education Pages publication OF THE SAME COMMIT. Both
    # workflows start from the same push and run concurrently, so the bound must
    # exceed how long a publication takes. Twelve consecutive runs on main
    # measured 6m20s at the fastest, ~7m50s typically, 26m17s at the slowest.
    #
    # The ceiling was 300s and the default 240s -- both below every one of those
    # twelve, so the step had never once been able to finish its measurement on a
    # push, and main read red for it every time. Raising the caller alone made it
    # worse, not better: the tool rejected 1800 against the old 300 ceiling and
    # failed instantly instead of after four minutes.
    #
    # WHAT THE CEILING IS FOR, since the 300 arrived with no comment, no test and
    # no recorded reason, and the next person deserves something to argue against:
    # it is the promise that this job cannot hold a runner indefinitely waiting on
    # another workflow that may never finish. It is NOT a statement about how long
    # a publication takes -- that is what the default is for. So the ceiling
    # should sit just under the job's timeout-minutes (a wait the job would kill
    # anyway is not a wait), and the default should sit above the slowest
    # publication actually measured. Raise the default when publications get
    # slower; raise the ceiling only when the job timeout rises with it.
    # tools/check_serve_proof_bounds.py enforces exactly that, and red-proves it.
    parser.add_argument('--wait-seconds', type=int, default=1800)
    args = parser.parse_args()
    require(1 <= args.wait_seconds <= 2400,
            'Publication wait must be bounded to 1–2400 seconds')
    roots = {'site': args.site, 'lessons': args.lessons, 'apps': args.apps, 'games': args.shelf}
    wanted = {kind: head(root) for kind, root in roots.items()}
    config = json.loads((args.shelf/'play-publication.json').read_text())
    require(config['domain'] == 'madebymatt-play.uk', 'Unrecognised declared games publication origin')
    games = json.loads((args.shelf/'games.json').read_text())['games']
    routes = [urllib.parse.unquote(urllib.parse.urlsplit(g['href']).path).removesuffix('index.html').rstrip('/') or '/' for g in games]
    require(routes and len(routes) == len(set(routes)), 'Canonical games publication membership is empty or duplicated')
    github = GitHub(time.monotonic() + args.wait_seconds)
    args.output.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {kind: pool.submit(prepare_one, kind, wanted[kind], args.output, github) for kind in roots}
        publications = {kind: task.result() for kind, task in futures.items()}
    result = {'version': 1, 'publications': publications, 'games_origin': 'https://' + config['domain'],
              'canonical_game_routes': routes}
    path = args.output/'publications.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(f'BOUND PUBLICATIONS {path}', flush=True)


if __name__ == '__main__':
    try:
        main()
    except Red as error:
        print('[RED] ' + str(error), file=sys.stderr)
        sys.exit(1)
    except Inconclusive as error:
        print('[INCONCLUSIVE] ' + str(error), file=sys.stderr)
        sys.exit(2)
