# Science exemplar authoring source

The three classroom ZIPs contain all 24 lessons in PowerPoint, Word, PDF and HTML. Standard classroom editing needs only PowerPoint, Word or compatible software.

This optional source archive preserves final lesson JSON, classic chassis, SVG/HTML interaction code, office generators, scheme references and validation reports. The final content JSON files are authoritative. Authoring scripts preserve how lessons were drafted and can predate final reviewed corrections; do not run them over edited content without reviewing their changes.

Rebuilding requires Python with python-docx, Pillow and PyMuPDF, Node with the presentation dependencies referenced by ppt.mjs, and the managed office renderer. Some runtime and skill paths are environment-specific and need adaptation elsewhere. Dependencies are not bundled.

Run the document, presentation and HTML generators against content JSON. Review regenerated diagrams, answers and page layouts before teaching. build/package.py makes eight-lesson pathway ZIPs and checks each stays below 20,000,000 bytes.

Animations are controllable SVG elements in the HTML lessons. Selected lessons extend their diagrams with model controls for investigation and explanation. Each of the 24 lessons also has three authored prediction/test/explanation decisions. Diagram transition timing is not a real scientific time scale. Interactive state changes passed automated checks; direct browser and physical-phone testing remains unverified.
