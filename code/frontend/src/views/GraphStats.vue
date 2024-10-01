<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <div class="card fixed-size-card">
        <div class="card-header">Statistics Overview</div>
        <div class="card-body">
          <div class="chart-container">
            <Bar :data="chartData" :options="chartOptions" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ChartDataLabels);

export default {
  components: {
    Bar,
    NavBar
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: []
      },
      chartOptions: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top'
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `${context.dataset.label}: ${context.raw}`;
              }
            }
          },
          datalabels: {
            color: '#000',
            anchor: 'end',
            align: 'top',
            formatter: (value, context) => {
              if (context.dataIndex === this.mostRequestedBookIndex) {
                return this.mostRequestedBookName; // Display the name of the most requested book
              }
              return '';
            },
            display: (context) => context.dataIndex === this.mostRequestedBookIndex // Only show label for the most requested book
          }
        },
        scales: {
          x: {
            beginAtZero: true
          },
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1 // Ensures the y-axis scale increments by 1
            }
          }
        }
      }
    };
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const response = await fetch('http://127.0.0.1:5000/admin/stats', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }
        const data = await response.json();
        this.updateChartData(data);
      } catch (error) {
        console.error('Error:', error);
      }
    },
    updateChartData(data) {
      this.mostRequestedBookIndex = 8; // Assuming the most requested book is at index 8
      this.mostRequestedBookName = data.most_requested_book_name; // Get the name of the most requested book from the API response
      this.chartData = {
        labels: [
          'Total Users',
          'Total Books',
          'Total Sections',
          'Pending Requests',
          'Accepted Requests',
          'Rejected Requests',
          'Revoked Requests',
          'Deleted Requests',
          'Most Requested Book'
        ],
        datasets: [
          {
            label: 'Statistics',
            backgroundColor: '#42A5F5',
            data: [
              data.total_users,
              data.total_books,
              data.total_sections,
              data.pending_requests,
              data.accepted_requests,
              data.rejected_requests,
              data.revoked_requests,
              data.deleted_requests,
              data.most_requested_book_count // Add this to the data
            ]
          }
        ]
      };
    }
  }
};
</script>

<style scoped>
.container {
  margin-top: 50px;
}

.fixed-size-card {
  width: 100%; /* Full width of the container */
  max-width: 1000px; /* Maximum width for larger screens */
  height: 500px; /* Increased height for better visibility */
  margin: 0 auto; /* Center the card horizontally */
}

.card-body {
  padding: 0; /* Remove default padding to use full height for chart */
}

.chart-container {
  width: 100%; /* Make the chart container fill the card width */
  height: 100%; /* Make the chart container fill the card height */
}
</style>
