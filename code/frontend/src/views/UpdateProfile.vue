<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <header>
        <h1>Update Profile</h1>
      </header>
      <div v-if="user" class="update-form">
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label for="name" class="form-label">Name:</label>
            <input v-model="user.name" type="text" class="form-control" id="name" required />
          </div>
          <div class="form-group">
            <label for="email">Email:</label>
            <input type="text" id="email" v-model="user.email" disabled />
          </div>
         
          <div class="form-group">
            <label for="role">Role:</label>
            <input type="text" id="role" v-model="user.role" disabled />
          </div>
          <div class="form-group">
            <label for="joined-date">Joined Date:</label>
            <input type="text" id="joined-date" v-model="formattedJoinedDate" disabled />
          </div>
          <button type="submit" class="btn btn-primary">Update Name</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import UserMixins from '../mixins/userMixins';

export default {
  components: {
    NavBar
  },
  mixins: [UserMixins],
  data() {
    return {
      user: null,
    };
  },
  computed: {
    formattedJoinedDate() {
      if (this.user && this.user.joined_date) {
        const date = new Date(this.user.joined_date);
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
        const day = String(date.getDate()).padStart(2, '0');
        const year = date.getFullYear();
        return `${month}/${day}/${year}`;
      }
      return '';
    }
  },
  created() {
    this.fetchUser();
  },
  methods: {
    fetchUser() {
      fetch(`http://127.0.0.1:5000/getuserinfo`)
        .then(response => response.json())
        .then(data => {
          this.user = data; // Directly assign fetched user data
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
        });
    },
    updateProfile() {
      const userId = this.user.id; // Retrieve user ID from the user object
      fetch(`http://127.0.0.1:5000/update-profile/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        body: JSON.stringify({ name: this.user.name }) // Send the updated name
      })
        .then(response => response.json())
        .then(data => {
          if (data.message) {
            alert('Profile updated successfully!');
            this.$router.push('/my-profile');
          } else {
            alert('Failed to update profile.');
          }
        })
        .catch(error => {
          console.error('Error updating profile:', error);
          alert('Failed to update profile.');
        });
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}

header {
  margin-top: 50px;
  background-color: #f2f2f2;
  padding: 20px;
  font-size: 24px;
  text-align: center;
  margin-bottom: 50px;
}

.update-form {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff; /* Primary color */
  color: white;
}
</style>
