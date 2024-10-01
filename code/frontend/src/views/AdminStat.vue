<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <h2>Admin Dashboard</h2>
      <h4 style="color:blue; font-weight:bold">Statistics</h4>
      <div class="row">
        <div class="col-md-4">
          <div class="card text-white bg-primary mb-3">
            <div class="card-header">Total Users</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.total_users }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-success mb-3">
            <div class="card-header">Total Books</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.total_books }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-info mb-3">
            <div class="card-header">Total Sections</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.total_sections }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-warning mb-3">
            <div class="card-header">Pending Requests</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.pending_requests }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-danger mb-3">
            <div class="card-header">Accepted Requests</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.accepted_requests }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-secondary mb-3">
            <div class="card-header">Rejected Requests</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.rejected_requests }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-danger mb-3">
            <div class="card-header">Revoked Requests</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.revoked_requests }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-secondary mb-3">
            <div class="card-header">Deleted Requests</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.deleted_requests }}</h5>
            </div>
          </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-primary mb-3">
            <div class="card-header">Most Requested Book</div>
            <div class="card-body">
              <h5 class="card-title">{{ stats.most_requested_book_name }}</h5>
              <p class="card-text">Requests: {{ stats.most_requested_book_count }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      stats: {
        total_users: 0,
        total_books: 0,
        total_sections: 0,
        pending_requests: 0,
        accepted_requests: 0,
        rejected_requests: 0,
        revoked_requests: 0,
        deleted_requests: 0,
        most_requested_book_name: '',
        most_requested_book_count: 0,
      },
    };
  },
  mounted() {
    this.getStats();
  },
  methods: {
    getStats() {
      fetch('http://127.0.0.1:5000/admin/stats', {
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
