fetch('/api/operational/stay-length-by-room')
  .then(res => res.json())
  .then(data => {
    if (!Array.isArray(data) || !data.length) return;
    const ctx = document.getElementById('stayLengthChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.map(item => item.room_type),
        datasets: [{
          label: 'Average Stay Duration (Days)',
          data: data.map(item => item.stay_duration),
          fill: false,
          borderColor: '#3949AB',
          backgroundColor: '#3949AB',
          tension: 0.3,
          borderWidth: 2,
          pointRadius: 4
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Average Stay Length by Room Type'
          },
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Avg Stay Duration (days)'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Room Type'
            }
          }
        }
      }
    });
  }); 