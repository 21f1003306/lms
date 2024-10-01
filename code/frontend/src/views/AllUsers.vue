<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <h2>All Registered Users</h2>
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Joined Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>{{ user.joined_date }}</td>
            <td>
              <div class="btn-group" role="group">
                <button v-if="role === 'admin'" class="btn btn-outline-danger" @click="deleteUser(user.id)">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  components: {
    NavBar
  },
  data() {
    return {
      users: [],
      role: '' // To store user role
    };
  },
  mounted() {
    this.getUsers();
    this.getUserRole(); // Fetch the user role
  },
  methods: {
    async getUsers() {
      try {
        const response = await fetch('http://127.0.0.1:5000/all-users', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          }
        });
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }
        const data = await response.json();
        // Filter out librarians and set only users
        this.users = data.filter(user => user.role === 'user');
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    async getUserRole() {
      try {
        const response = await fetch('http://127.0.0.1:5000/getuserinfo', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          }
        });
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }
        const data = await response.json();
        this.role = data.role;
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    },
    async deleteUser(userId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/delete-user/${userId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json',
          },
        });
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || `HTTP error: ${response.status}`);
        }
        const data = await response.json();
        alert(data.message);
        this.getUsers(); // Refresh the list of users after deletion
      } catch (error) {
        alert(`Error deleting user: ${error.message}`);
        console.error(`Error deleting user with ID ${userId}:`, error);
      }
    }
  }
};
</script>

<style scoped>
/* Add your styles here if needed */
</style>
