<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <h2>My Feedbacks</h2>
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Book Id</th>
            <th>Book Name</th>
            <th>Rating</th>
            <th>Comment</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="feedback in feedbacks" :key="feedback.id">
            <td>{{ feedback.id }}</td>
            <td>{{ feedback.book_id }}</td>
            <td>{{ feedback.book_name }}</td>
            <td>
              <div class="rating-strip">
                <span
                  v-for="star in stars"
                  :key="star"
                  :class="{
                    selected: star <= feedback.rating
                  }"
                >
                  ★
                </span>
              </div>
            </td>
            <td>{{ feedback.comment }}</td>
            <td>{{ formatDate(feedback.feedback_date) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import UserMixins from '../mixins/userMixins';

export default {
  mixins: [UserMixins],
  components: {
    NavBar
  },
  data() {
    return {
      feedbacks: [],
      stars: [1, 2, 3, 4, 5],
    };
  },
  mounted() {
    this.getFeedbacks();
  },
  methods: {
    getFeedbacks() {
      fetch('http://127.0.0.1:5000/my-feedbacks', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
        .then(response => response.json())
        .then(data => {
          this.feedbacks = data;
        })
        .catch(error => {
          console.error('Error fetching feedbacks:', error);
        });
    },
    formatDate(dateString) {
    const options = { day: '2-digit', month: 'short', year: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', options);
  }
  },
};
</script>

<style scoped>
.rating-strip {
  display: justify;
  font-size: 2rem; /* Adjust size as needed */
  color: grey; /* Default star color */
}

.rating-strip span.selected {
  color: #007bff; /* Color for selected stars */
}
</style>
