'use strict';
document.documentElement.classList.add('js');
const printButton=document.querySelector('[data-print-task]');
const answerChoice=document.querySelector('[data-print-answers]');
let answerStates=[];
function preparePrint(){
  document.body.classList.toggle('print-answers',Boolean(answerChoice&&answerChoice.checked));
  answerStates=Array.from(document.querySelectorAll('details.answer')).map(node=>({node,open:node.open}));
  if(answerChoice&&answerChoice.checked)for(const {node} of answerStates)node.open=true;
}
function finishPrint(){
  for(const {node,open} of answerStates)node.open=open;
  answerStates=[];
  document.body.classList.remove('print-answers');
}
window.addEventListener('beforeprint',preparePrint);
window.addEventListener('afterprint',finishPrint);
if(printButton)printButton.addEventListener('click',()=>window.print());
// Native details, links and video controls work without this enhancement.
// Responses stay in this document only. No storage, analytics or submissions.
