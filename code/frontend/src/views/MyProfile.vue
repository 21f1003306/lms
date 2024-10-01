<template>
  <NavBar />
  <div>
    <header>
      <h1>My Profile</h1>
    </header>
    <div v-if="user">
      <div v-if="user" class="profile-card">
      <div class="profile-info">
        <p><h5><strong>Name:</strong> {{ user.name }}</h5></p>
        <p><h5><strong>Email:</strong> {{ user.email }}</h5></p>
        <p><h5><strong>Role:</strong> {{ user.role }}</h5></p>
        <p><h5><strong>User Id:</strong> {{ user.id }}</h5></p>
        <p><h5><strong>Joined Date:</strong> {{ formattedJoinedDate }}</h5></p>
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
    NavBar
  },
  mixins: [UserMixins],
  data() {
    return {
      user: null
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
    async fetchUser() {
      try {
        const userId = 1; // Replace with actual user ID, possibly from route params or auth context
        
        this.user = response.data;
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    }
  }
};
</script>

<style scoped>
header {
  margin-top: 50px;
  background-color: #f2f2f2;
  padding: 20px;
  font-size: 24px;
  text-align: center;
  margin-bottom: 50px;
}

.profile-card {
  display: flex;
  justify-content: center;
  background-color: #007bff; /* Primary color */
  color: white;
  border-radius: 8px;
  padding: 20px;
  width: 100%;
  max-width: 1000px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-left: auto;
  margin-right: auto;
  
}
</style>
