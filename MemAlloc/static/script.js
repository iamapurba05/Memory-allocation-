const $ = id => document.getElementById(id);
let results = [], selected = 'First Fit';
const examples = {
  fragment: [[100, 100, 100], [150]],
  exact: [[100, 200], [100, 200]],
  fail: [[100, 200], [400]]
};
function sizes(value) {
  const parts = value.split(',').map(v => v.trim());
  if (parts.length > 30 || parts.some(v => !/^\d+$/.test(v) || Number(v) < 1 || Number(v) > 1000000)) {
    throw new Error('Enter 1–30 positive integer sizes (1–1,000,000 KB), separated by commas.');
  }
  return parts.map(Number);
}
function format(n) { return n.toLocaleString('en-US'); }
function metric(name, value, detail) {
  return `<div class="metric"><small>${name}</small><strong>${value}</strong><span>${detail}</span></div>`;
}
function segment(size, total, type, label) {
  if (!size) return '';
  return `<div class="segment ${type}" style="width:${size / total * 100}%" title="${label}: ${size} KB">${size / total >= .12 ? label : ''}</div>`;
}
async function run() {
  $('error').textContent = '';
  $('run').disabled = true;
  try {
    const payload = {blocks: sizes($('blocks').value), processes: sizes($('processes').value), mode: $('mode').value};
    const response = await fetch('/api/simulate', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Simulation failed.');
    results = data.results;
    $('results').hidden = false;
    render();
  } catch (e) {
    $('error').textContent = e.message;
    results = [];
    $('results').hidden = true;
  } finally { $('run').disabled = false; }
}
function render() {
  if (!results.length) return;
  const r = results.find(v => v.method === selected);
  document.querySelectorAll('[data-method]').forEach(b => {b.classList.toggle('active', b.dataset.method === selected); b.setAttribute('aria-pressed', b.dataset.method === selected);});
  $('metrics').innerHTML = metric('Total memory', `${format(r.total)} KB`, 'Original capacity') +
    metric('Allocated memory', `${format(r.used)} KB`, `${r.utilization}% utilization`) +
    metric('Free memory', `${format(r.free)} KB`, `Largest hole: ${format(r.largest)} KB`) +
    metric('Processes allocated', `${r.allocated} / ${r.allocated+r.failed}`, `${r.success_rate}% success`);
  $('memory').innerHTML = r.blocks.map(b => `<div class="block"><span class="block-label">Block ${b.id}</span><div class="bar">${b.allocations.map(a => segment(a.size,b.capacity,'used',`P${a.process}`)).join('')}${segment(b.internal,b.capacity,'waste','Waste')}${segment(b.remaining,b.capacity,'free','Free')}</div><span class="block-size">${format(b.remaining)} / ${format(b.capacity)} KB</span></div>`).join('');
  $('trace').innerHTML = r.trace.map(t => `<details><summary><strong>P${t.process}</strong><span>${format(t.size)} KB</span><span class="${t.block===null?'bad':'ok'}">${t.block===null?'Not allocated':'Block '+t.block} ▸</span></summary><div class="trace-detail"><div><strong>Decision:</strong> ${t.reason}</div><div><strong>Before:</strong> [${t.before.join(', ')}] KB</div><div><strong>Blocks checked:</strong> ${t.inspected.join(', ')}</div><div><strong>Suitable blocks found:</strong> ${t.candidates.join(', ') || 'None'}</div><div><strong>After:</strong> [${t.after.join(', ')}] KB</div></div></details>`).join('');
  $('comparison').innerHTML = `<div class="table-wrap"><table><thead><tr><th>Algorithm</th><th>Allocated</th><th>Failed</th><th>Used (KB)</th><th>Free (KB)</th><th>Internal (KB)</th><th>Block checks</th></tr></thead><tbody>${results.map(v=>`<tr><td>${v.method}</td><td>${v.allocated}</td><td>${v.failed}</td><td>${format(v.used)}</td><td>${format(v.free)}</td><td>${format(v.internal)}</td><td>${v.checks}</td></tr>`).join('')}</tbody></table></div><p class="hint" style="margin-top:14px">Useful memory utilization (%)</p>${results.map(v=>`<div class="chart-row"><span>${v.method}</span><div class="chart-bar"><div style="width:${v.utilization}%"></div></div><strong>${v.utilization}%</strong></div>`).join('')}`;
  const bestCount = Math.max(...results.map(v=>v.allocated));
  const leaders = results.filter(v=>v.allocated===bestCount);
  const lowest = Math.min(...leaders.map(v=>v.checks));
  const efficient = leaders.filter(v=>v.checks===lowest);
  $('observation').textContent = `For this workload, ${leaders.map(v=>v.method).join(', ')} allocated the most processes (${bestCount}). Among these, ${efficient.map(v=>v.method).join(', ')} required the fewest block checks (${lowest}). This is workload-dependent, not a universal ranking.`;
  const frag = r.mode==='dynamic' ? r.trace.filter(t=>t.reason.startsWith('External fragmentation')).length : 0;
  $('fragmentation').innerHTML = `<div class="frag-grid"><div><small>Internal fragmentation</small><strong>${format(r.internal)} KB</strong></div><div><small>External index</small><strong>${r.external_index===null?'N/A':r.external_index+'%'}</strong></div><div><small>${r.mode==='dynamic'?'Failures due to external fragmentation':'Total failed requests'}</small><strong>${r.mode==='dynamic'?frag:r.failed}</strong></div></div><p>${r.mode==='dynamic'?'Dynamic model: holes are split exactly, so internal waste is zero (no rounding or metadata). External index = 100 × (1 − largest free hole / total free memory); zero when no free memory exists. Separate holes cannot be combined in this model.':'Fixed model: one process occupies each partition. Unused space inside occupied partitions is internal waste and cannot be reused. External index is not applied in this mode.'}</p><p style="margin-top:8px">Capacity check: ${format(r.used)} allocated + ${format(r.internal)} internal waste + ${format(r.free)} free = ${format(r.total)} KB.</p>`;
}
$('form').addEventListener('submit', e=>{e.preventDefault();run();});
$('mode').addEventListener('change', ()=>{$('modeHint').textContent = $('mode').value==='dynamic'?'A suitable free hole is split; its remainder is reusable.':'Each partition holds at most one process. Leftover space is internal waste.';});
document.querySelectorAll('[data-method]').forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.method;render();}));
document.querySelectorAll('[data-example]').forEach(b=>b.addEventListener('click',()=>{const [blocks,processes]=examples[b.dataset.example];$('blocks').value=blocks.join(', ');$('processes').value=processes.join(', ');$('mode').value='dynamic';$('mode').dispatchEvent(new Event('change'));run();}));
$('reset').addEventListener('click',()=>{$('blocks').value='100, 500, 200, 300, 600';$('processes').value='212, 417, 112, 426';$('mode').value='dynamic';$('mode').dispatchEvent(new Event('change'));selected='First Fit';run();});
$('export').addEventListener('click',()=>{if(!results.length)return;const rows=[['Algorithm','Model','Allocated','Failed','Used KB','Free KB','Internal waste KB','External index %','Success %','Utilization %','Block checks'],...results.map(r=>[r.method,r.mode,r.allocated,r.failed,r.used,r.free,r.internal,r.external_index??'N/A',r.success_rate,r.utilization,r.checks])];const blob=new Blob([rows.map(r=>r.join(',')).join('\n')+'\n'],{type:'text/csv'});const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='memory-comparison.csv';link.click();setTimeout(()=>URL.revokeObjectURL(link.href),1000);});
run();
