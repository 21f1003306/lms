<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <h2>User Dashboard</h2>
      <h4 style="color:blue; font-weight:bold">User Statistics</h4>
      <div class="row">
        <div class="col-md-4">
          <div class="card text-white bg-primary mb-3">
            <div class="card-header">Total Books Requested</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.total_requested }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-success mb-3">
            <div class="card-header">Total Books Accepted</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.total_accepted }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-info mb-3">
            <div class="card-header">Total Books Read/Returned</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.total_read }}</h5>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import UserMixins from '../mixins/userMixins';

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      stats: {
        total_requested: 0,
        total_accepted: 0,
        total_read: 0,
      },
    };
  },
  mounted() {
    this.getUserStats();
  },
  methods: {
    getUserStats() {
      const userId = localStorage.getItem('user_id');  // Assuming user_id is stored in localStorage
      fetch(`http://127.0.0.1:5000/user/stats?user_id=${userId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          this.stats = data;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}
.card {
  margin-bottom: 20px;
}
</style>
