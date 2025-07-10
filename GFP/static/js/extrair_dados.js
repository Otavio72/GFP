document.addEventListener("DOMContentLoaded", () => {
  // Verifica se a seção existe antes de continuar
  const dadosElement = document.getElementById('dados_extraidos');
  if (!dadosElement) return;

  const dados = JSON.parse(dadosElement.textContent);
  console.log('DADOS:', dados);

  const agrupado = {};
  dados.forEach(item => {
    const nome = item.tipo_conta;
    const valor = parseFloat(item.boleto_valor);
    agrupado[nome] = (agrupado[nome] || 0) + valor;
  });

  // Inicializa Swiper
  const swiper = new Swiper('.Swiper_extrair_dados', {
    loop: true,
    slidesPerView: 1,
    spaceBetween: 0,
    centeredSlides: false,
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });

  // Inicializa os gráficos
  initCharts(dados, agrupado);
});

function initCharts(dados, agrupado) {
  const ctxPizza = document.getElementById('graficoPizza')?.getContext('2d');
  const ctxRadar = document.getElementById('graficoRadar')?.getContext('2d');
  const ctxLinha = document.getElementById('graficoLinhas')?.getContext('2d');

  if (!ctxPizza || !ctxRadar || !ctxLinha) return;

  const labels = Object.keys(agrupado);
  const valores = Object.values(agrupado);

  // Gráfico Pizza
  new Chart(ctxPizza, {
    type: 'pie',
    data: {
      labels,
      datasets: [{
        label: 'Valor',
        data: valores,
        backgroundColor: ['#daa520', '#8a0303', '#D2691E'],
        borderColor: '#fff',
        borderWidth: 2,
        borderRadius: 10,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: { color: '#333', font: { size: 14 }, display: true }
        },
        tooltip: {
          backgroundColor: '#B2222',
          titleColor: '#FFD700',
          bodyColor: '#fff'
        }
      }
    }
  });

console.log('AGRUPADO antes do radar', agrupado);
console.log('labels antes do radar', labels);
  // Gráfico Radar
  new Chart(ctxRadar, {
    type: 'radar',
    data: {
      labels,
      datasets: [{
        label: 'Valores',
        data: valores,
        backgroundColor: 'rgba(255, 180, 0, 0.4)',
        borderColor: '#8a0303',
        borderWidth: 2
      }]
    },
    options: {
      scales: {
        r: {
          angleLines: { color: '#000000' },
          grid: { color: '#000000' },
          pointLabels: { color: '#000000', font: { size: 10 } },
          ticks: { backdropColor: 'rgba(255, 255, 255, 0.8)' }
        }
      },
      plugins: {
        legend: { display: true }
      }
    }
  });

  // Gráfico Linhas
  const agrupadoPorTipo_conta= {};
  dados.forEach(item => {
    const nome = item.tipo_conta;
    const data = item.boleto_data;
    const valor = parseFloat(item.boleto_valor);

    if (!agrupadoPorTipo_conta[nome]) {
      agrupadoPorTipo_conta[nome] = [];
    }

    agrupadoPorTipo_conta[nome].push({ data, valor });
  });

  const todasDatas = [...new Set(dados.map(item => item.boleto_data))].sort();

  const cores = ['#8a0303', '#daa520', '#1e90ff', '#228b22', '#800080'];
  const datasets = [];
  let corIndex = 0;

  for (const [nome, valores] of Object.entries(agrupadoPorTipo_conta)) {
    const valorPorData = Object.fromEntries(valores.map(v => [v.data, v.valor]));
    const dadosOrdenados = todasDatas.map(data => valorPorData[data] || 0);

    datasets.push({
      label: nome,
      data: dadosOrdenados,
      borderColor: cores[corIndex % cores.length],
      backgroundColor: cores[corIndex % cores.length] + '55',
      fill: true,
      borderWidth: 2,
      tension: 0.3
    });

    corIndex++;
  }

  let fundoGradient = ctxLinha.createLinearGradient(0, 0, 0, 400);
  fundoGradient.addColorStop(0, 'rgba(255,0,0,0.1)');
  fundoGradient.addColorStop(1, 'rgba(255,215,0,0.1)');

  new Chart(ctxLinha, {
    type: 'line',
    data: {
      labels: todasDatas,
      datasets
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}