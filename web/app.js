"use strict";
const runs = JSON.parse(document.querySelector("#benchmark-data").textContent);
const $ = s => document.querySelector(s);
const esc = x => String(x ?? "—").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const pct = x => x == null ? "À relire" : `${(x * 100).toFixed(1)} %`;
const num = x => x == null ? "Non mesuré" : x.toFixed(2);
const labels = {extraction:"Extraction",chronology:"Chronologie",synthesis:"Synthèse"};
let current = runs.length - 1;
function safeURL(url) { try { const u=new URL(url);return u.protocol==="https:"?u.href:"#"; } catch { return "#"; } }
function render() {
  const run = runs[current];
  if (!run) { $("#comparison").textContent = "Aucune exécution disponible."; return; }
  $("#run-status").textContent = `${run.split === "dev" ? "Mise au point" : "Pilote"} · ${{completed:"Terminée",running:"En cours",interrupted:"Interrompue"}[run.status]||run.status} · ${new Date(run.created_at).toLocaleString("fr-FR")}`;
  const nCases=new Set(run.results.map(r=>r.case_id)).size;
  const nModels=new Set(run.results.filter(r=>r.provider==="ollama").map(r=>r.model)).size;
  $("#kpis").innerHTML = [["MODÈLES LOCAUX",nModels,"Versions et empreintes enregistrées"],["CAS DISTINCTS",nCases,`${new Set(run.cases.map(c=>c.source_id)).size} rapports dans cet ensemble`],["RÉPONSES CONSERVÉES",run.results.length,"Règles et répétitions incluses"],["FRAIS D’API","0 €","Énergie et matériel non chiffrés"]].map(([label,value,sub])=>`<div class="kpi"><div class="label">${label}</div><div class="value">${value}</div><div class="sub">${sub}</div></div>`).join("");
  $("#comparison").innerHTML=Object.entries(labels).map(([task,label])=>{
    const rows=run.aggregates.filter(r=>r.task===task);
    if(!rows.length)return "";
    return `<h3>${label}</h3><div class="table-wrap"><table><thead><tr><th>Modèle</th><th>Cas / réponses</th><th>Exactitude des champs</th><th>Format conforme</th><th>Erreurs critiques¹</th><th>Échecs d’exécution</th><th>Latence médiane</th><th>Variation²</th></tr></thead><tbody>${rows.map(r=>`<tr><td class="model">${esc(r.model)} ${r.model.startsWith("regex")?'<span class="pill">Règles</span>':""}</td><td>${r.distinct_cases} / ${r.n}</td><td>${pct(r.field_accuracy)}${r.field_accuracy==null?' <span class="pill warn">Relecture</span>':`<div class="bar-track"><div class="bar" style="width:${100*r.field_accuracy}%"></div></div>`}</td><td>${pct(r.format_rate)}</td><td>${task==="synthesis"?"Non notées":r.critical_errors}</td><td>${pct(r.error_rate)}</td><td>${num(r.latency_median_s)} s</td><td>${r.mean_repeat_range==null?"—":pct(r.mean_repeat_range)}</td></tr>`).join("")}</tbody></table></div>`;
  }).join("")+`<p class="footnote">¹ Champs critiques incorrects parmi les réponses analysables ; les erreurs de format et d’exécution sont affichées séparément. ² Écart moyen entre meilleure et moins bonne exactitude d’un même cas, en points de pourcentage.</p>`;
  $("#model-filter").innerHTML='<option value="">Tous les modèles</option>'+[...new Set(run.results.map(r=>r.model))].map(m=>`<option value="${esc(m)}">${esc(m)}</option>`).join("");
  $("#source-cards").innerHTML=run.sources.map(s=>`<article class="card"><span class="pill ${s.split==="dev"?"warn":""}">${s.split==="dev"?"Mise au point":"Pilote"}</span><h3>${esc(s.campaign)}</h3><p>${esc(s.title)}</p><p>Version : <strong>${esc(s.document_date)}</strong><br>Collecte : ${esc(s.retrieved_at)}<br>Origine : ${esc(s.origin)}</p><a href="${esc(safeURL(s.url))}" target="_blank" rel="noopener noreferrer">Consulter le rapport original ↗</a><p class="hash">SHA-256 · ${esc(s.sha256)}</p></article>`).join("");
  $("#provenance").textContent=JSON.stringify({protocol:run.protocol_version,corpus_hash:run.corpus_hash,cases_hash:run.cases_hash,models:run.models,environment:run.environment},null,2);
  renderCases();
}
function renderCases(){
  const run=runs[current];if(!run)return;
  const model=$("#model-filter").value,task=$("#task-filter").value;
  const rows=run.results.map((r,i)=>({...r,index:i})).filter(r=>(!model||r.model===model)&&(!task||r.task===task));
  $("#case-list").innerHTML=rows.map(r=>`<button class="case-button" data-index="${r.index}"><strong>${esc(r.case_id)}</strong><small>${esc(r.model)} · essai ${r.repeat+1}</small><small>${r.status!=="ok"?esc(r.status):r.task==="synthesis"?"Qualité : relecture requise":`Champs : ${pct(r.score?.field_accuracy??0)}`}</small></button>`).join("");
  document.querySelectorAll(".case-button").forEach(b=>b.addEventListener("click",()=>detail(Number(b.dataset.index))));
  if(rows.length)detail(rows[0].index);else $("#detail").textContent="Aucune réponse pour ces filtres.";
}
function detail(index){
  const run=runs[current],r=run.results[index],c=run.cases.find(c=>c.id===r.case_id),s=run.sources.find(s=>s.id===c.source_id);
  document.querySelectorAll(".case-button").forEach(b=>b.classList.toggle("active",Number(b.dataset.index)===index));
  const metrics=r.metrics||{};
  const evidence=c.expected?Object.entries(c.expected).map(([key,v])=>`<div class="evidence"><strong>${esc(key)}</strong> → ${esc(JSON.stringify(v.value))} ${v.critical?'<span class="pill warn">Critique</span>':""}<br>p. ${v.page} · ${esc(v.quote)}</div>`).join(""):c.rubric.map(v=>`<div class="evidence"><strong>${esc(v.criterion)}</strong><br>p. ${v.page} · ${esc(v.quote)}</div>`).join("");
  const score=r.score||{};
  $("#detail").innerHTML=`<p class="eyebrow">${esc(labels[c.task])} / ${esc(c.id)}</p><h3>${esc(c.title)}</h3><div class="detail-meta"><span class="pill">${esc(r.model)}</span><span class="pill">Essai ${r.repeat+1}</span><span class="pill ${r.status==="ok"?"":"warn"}">${esc(r.status)}</span></div><p>${esc(c.instruction)}</p><p><a href="${esc(safeURL(s.url))}" target="_blank" rel="noopener noreferrer">Source ${esc(s.campaign)} · ${esc(s.document_date)} ↗</a></p><h4>Réponse brute</h4><pre>${esc(r.raw_response||r.error||"Réponse vide")}</pre><div class="review-note">${c.task==="synthesis"?"Qualité sémantique non notée. Appliquer la grille ci-dessous avec un évaluateur humain.":"Une citation retrouvée dans le texte n’est pas nécessairement une preuve pertinente. Sa pertinence reste à relire."}</div>${score.details?.length?`<h4>Contrôles automatiques par champ</h4><div class="table-wrap"><table><thead><tr><th>Champ</th><th>Valeur</th><th>Citation retrouvée</th></tr></thead><tbody>${score.details.map(d=>`<tr><td>${esc(d.field)}</td><td class="${d.correct?"correct":"incorrect"}">${d.correct?"Conforme":"Incorrecte / absente"}</td><td>${d.quote_valid?"Oui":"Non"}</td></tr>`).join("")}</tbody></table></div>`:""}<h4>Références et critères de relecture</h4>${evidence}<details><summary>Mesures, paramètres et notation détaillée</summary><pre>${esc(JSON.stringify({metrics,parameters:r.parameters,done_reason:r.done_reason,score},null,2))}</pre></details>`;
}
document.querySelectorAll("[data-tab]").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll("[data-tab]").forEach(n=>n.classList.toggle("active",n===b));
  document.querySelectorAll(".view").forEach(v=>v.hidden=v.id!==b.dataset.tab);
}));
$("#run-select").innerHTML=runs.map((r,i)=>`<option value="${i}">${r.split==="dev"?"Mise au point":"Pilote"} · ${esc(r.run_id)}</option>`).join("");
$("#run-select").value=String(current);
$("#run-select").addEventListener("change",e=>{current=Number(e.target.value);render();});
$("#model-filter").addEventListener("change",renderCases);$("#task-filter").addEventListener("change",renderCases);
render();
