const params=new URLSearchParams(location.search);
const local=['localhost','127.0.0.1'].includes(location.hostname);
const API=params.get('api')||(local?'http://localhost:8000':'');
const OPS=params.has('ops');
const $=s=>document.querySelector(s), $$=s=>document.querySelectorAll(s);
if(OPS) $$('[data-ops-only]').forEach(el=>el.hidden=false);
function tab(id,instant){
  if(id==='dashboard'&&!OPS) id='join';
  if(id==='survey') id='join';
  $$('.panel').forEach(x=>x.classList.toggle('active',x.id===id));
  $$('[data-tab]').forEach(b=>b.classList.toggle('on',b.dataset.tab===id));
  const panel=document.getElementById(id);
  const chrome=$('.chrome');
  const offset=chrome?chrome.getBoundingClientRect().height:0;
  if(panel){
    const top=panel.getBoundingClientRect().top+window.scrollY-offset-8;
    scrollTo({top:Math.max(0,top),behavior:instant?'auto':'smooth'});
  }
}
$$('[data-tab]').forEach(b=>b.onclick=()=>tab(b.dataset.tab));
$$('[data-go]').forEach(b=>b.onclick=()=>tab(b.dataset.go));
const start=params.get('tab')||location.hash.replace('#','');
if(start) tab(start,true);
else $$('[data-tab="concept"]').forEach(b=>b.classList.add('on'));
async function request(path,options={}){
  const r=await fetch(API+path,{headers:{'Content-Type':'application/json'},...options});
  const data=await r.json();
  if(!r.ok) throw new Error(typeof data.detail==='string'?data.detail:JSON.stringify(data.detail)||'API error');
  return data;
}
$('#joinForm').onsubmit=async e=>{
  e.preventDefault();
  const f=new FormData(e.target);
  const modes=f.getAll('mode');
  const ages=f.getAll('required');
  const target=f.get('target');
  if(!target){ $('#joinResult').textContent='希望する相手を選んでください。'; return; }
  if(!modes.length){ $('#joinResult').textContent='興味のあるモードを1つ以上選んでください。'; return; }
  if(!ages.length){ $('#joinResult').textContent='希望年齢帯を1つ以上選んでください。'; return; }
  try{
    const created=await request('/v1/participants',{method:'POST',body:JSON.stringify({
      gender_identity:f.get('gender_identity'),
      target_genders:[target],
      role:f.get('role'),
      age_band:f.get('age_band'),
      area:f.get('area'),
      interested_modes:modes,
      required_age_bands:ages,
      preferred_age_bands:ages,
      availability:['2026-10-03T10','2026-10-04T13','2026-10-10T10'],
      portrait_opt_in:f.has('portrait_opt_in')
    })});
    await request('/v1/surveys',{method:'POST',body:JSON.stringify({
      participant_id:created.id,
      participation_intent:+f.get('participation_intent'),
      payment_intent:+f.get('payment_intent'),
      price_plan:f.get('price_plan'),
      comment:f.get('comment')||''
    })});
    $('#joinResult').textContent='送信しました。ご協力ありがとうございます。';
    if(OPS) loadKpi();
  }catch(err){
    $('#joinResult').textContent=err.message;
  }
};
async function loadKpi(){
  if(!OPS||!$('#kpis')) return;
  try{
    const d=await request('/v1/kpis');
    const labels={participation_intent_rate:'参加意向',payment_intent_rate:'支払意思',portrait_approval_rate:'似顔絵承認',formation_rate:'編成成立'};
    $('#kpis').innerHTML=Object.entries(labels).map(([k,v])=>`<div><b>${v}</b><h3>${Math.round(d[k]*100)}%</h3><small>基準 ${Math.round(d.thresholds[k]*100)}%</small></div>`).join('');
  }catch{
    $('#kpis').innerHTML='<div>API起動後に表示します</div>';
  }
}
if(OPS){
  $('#simulate').onclick=async()=>{
    try{$('#simulation').textContent=JSON.stringify(await request('/v1/simulations',{method:'POST'}),null,2);loadKpi()}
    catch(e){$('#simulation').textContent=e.message}
  };
  $('#kpis').innerHTML='<div>「匿名編成を実行」を押すと最新KPIを表示します</div>';
}
