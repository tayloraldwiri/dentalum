'use strict';
(() => {
  const planner = document.querySelector('#smile-planner');
  if (!planner) return;
  const goals = {
    care: {
      title: 'Ett friskt leende börjar med bra vanor.',
      description: 'Regelbundna undersökningar och förebyggande tandvård hjälper dig att ta hand om din munhälsa. En tandläkare eller tandhygienist kan hjälpa dig att hitta en rutin som passar dig.',
      caption: 'Små vanor. Stor skillnad över tid.',
      links: [['Basundersökning', 'basundersokning'], ['Tandhygienist', 'tandhygienist']]
    },
    align: {
      title: 'Utforska vägen till rakare tänder.',
      description: 'Tandreglering kan förändra tändernas position och hur de möts. Metod och behandlingstid beror på dina förutsättningar och behöver bedömas av en tandläkare.',
      caption: 'En ny position. Samma personliga leende.',
      links: [['Tandreglering', 'tandreglering'], ['Basundersökning', 'basundersokning']]
    },
    replace: {
      title: 'När något saknas finns det vägar framåt.',
      description: 'En saknad tand kan i vissa fall ersättas med ett implantat eller en bro. Din munhälsa, käkbenet och tänderna runt omkring påverkar vilka alternativ som är möjliga.',
      caption: 'Utforska alternativ för en saknad tand.',
      links: [['Tandimplantat', 'tandimplantat'], ['Kronor och broar', 'kronor-och-broar']]
    },
    bright: {
      title: 'Ett ljusare leende, på dina villkor.',
      description: 'Nyfiken på tändernas färg eller utseende? Läs om tandblekning och estetisk tandvård. En undersökning behövs för att bedöma din munhälsa och om en behandling är lämplig.',
      caption: 'Dina önskemål. Ett personligt uttryck.',
      links: [['Tandblekning', 'tandblekning'], ['Estetisk tandvård', 'estetisk-tandvard']]
    }
  };
  const controls = [...planner.querySelectorAll('button[data-goal]')];
  function selectGoal(key) {
    const goal = goals[key];
    if (!goal) return;
    planner.dataset.goal = key;
    controls.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.goal === key)));
    planner.querySelector('#planner-title').textContent = goal.title;
    planner.querySelector('#planner-description').textContent = goal.description;
    planner.querySelector('#planner-map-caption').textContent = goal.caption;
    planner.querySelector('#planner-counter').textContent = `0${Object.keys(goals).indexOf(key) + 1} / 04`;
    const links = goal.links.map(([label, route]) => {
      const link = document.createElement('a');
      link.href = `/behandlingar/${route}/`;
      link.append(document.createTextNode(label + ' '));
      const arrow = document.createElement('span');
      arrow.setAttribute('aria-hidden', 'true');
      arrow.textContent = '↗';
      link.append(arrow);
      return link;
    });
    planner.querySelector('#planner-links').replaceChildren(...links);
  }
  controls.forEach(button => button.addEventListener('click', () => selectGoal(button.dataset.goal)));
  planner.classList.add('is-ready');
})();
