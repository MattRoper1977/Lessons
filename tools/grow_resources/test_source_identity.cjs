/* Exercise the actual browser gate's source verifier with isolated fixtures.
 * The source tree is read-only; only temporary copies or links are changed.
 */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const {spawnSync}=require('node:child_process');
const {verifyInputs}=require('./browser_checks.cjs');
const targetPath='tools/grow_resources/BROWSER_TARGETS.json';
const contentPath='tools/grow_resources/CONTENT.json';
const readInputs=root=>({root,
  targets:JSON.parse(fs.readFileSync(path.join(root,targetPath),'utf8')),
  content:JSON.parse(fs.readFileSync(path.join(root,contentPath),'utf8'))});

if(process.argv[2]==='--verify-fixture'){
  const inputs=readInputs(process.argv[3]);
  verifyInputs(inputs);
  console.log(JSON.stringify({result:'PASS',verifiedFiles:inputs.targets.files.length}));
}else{
  assert.ok(process.argv.length===2||(process.argv.length===4&&process.argv[2]==='--root'),
    'Usage: node test_source_identity.cjs [--root SOURCE_TREE]');
  const sourceRoot=fs.realpathSync(process.argv[3]||path.join(__dirname,'../..'));
  const inputs=readInputs(sourceRoot);
  const fixture=fs.mkdtempSync(path.join(os.tmpdir(),'grow-source-identity-'));
  const records=[];
  function verify(label,defectPath){
    const run=spawnSync(process.execPath,[__filename,'--verify-fixture',fixture],{encoding:'utf8'});
    if(run.error)throw run.error;
    if(defectPath){
      assert.equal(run.status,1,'The planted '+label+' must redden the actual verifier');
      assert.ok(run.stderr.includes('Source identity: '+defectPath),
        'The failure must identify the deliberately changed source, not an unrelated error');
      records.push({case:label,expected:'FAIL',exitCode:run.status,
        assertion:run.stderr.split('\n').find(line=>line.includes('AssertionError')&&line.includes('Source identity:'))});
    }else{
      assert.equal(run.status,0,label+' must pass: '+run.stderr);
      records.push({case:label,expected:'PASS',exitCode:run.status,
        verifiedFiles:JSON.parse(run.stdout.trim()).verifiedFiles});
    }
  }
  try{
    for(const row of inputs.targets.files){
      const destination=path.join(fixture,row.path);
      fs.mkdirSync(path.dirname(destination),{recursive:true});
      fs.symlinkSync(path.join(sourceRoot,row.path),destination);
    }
    for(const relative of [targetPath,contentPath]){
      const destination=path.join(fixture,relative);
      fs.mkdirSync(path.dirname(destination),{recursive:true});
      fs.copyFileSync(path.join(sourceRoot,relative),destination);
    }
    const originalMetadata=fs.readFileSync(path.join(fixture,targetPath));
    verify('reviewed sources');
    // One companion and one original exercise both classes using the same
    // strict verifier. Selection is based on the manifest, not on a PR number.
    for(const relative of [inputs.targets.pages.at(-1).path,inputs.targets.lessons.at(-1).path]){
      const destination=path.join(fixture,relative);
      const original=fs.readFileSync(destination);
      fs.unlinkSync(destination); // Never write through the source-tree link.
      fs.writeFileSync(destination,original);
      try{
        fs.appendFileSync(destination,'\n<!-- planted source byte defect -->\n');
        verify('changed source bytes: '+relative,relative);
      }finally{fs.writeFileSync(destination,original);}
      verify('restored source bytes: '+relative);
      try{
        const metadata=JSON.parse(originalMetadata);
        const row=metadata.files.find(item=>item.path===relative);
        assert.ok(row,'The selected source must have a reviewed identity');
        row.sha256='0'.repeat(64);
        fs.writeFileSync(path.join(fixture,targetPath),JSON.stringify(metadata));
        verify('wrong expected digest: '+relative,relative);
      }finally{fs.writeFileSync(path.join(fixture,targetPath),originalMetadata);}
      verify('restored expected digest: '+relative);
    }
    console.log(JSON.stringify({result:'PASS',sourceRoot,cases:records},null,2));
  }finally{fs.rmSync(fixture,{recursive:true,force:true});}
}
