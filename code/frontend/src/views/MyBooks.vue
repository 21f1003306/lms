<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <h2>My Books</h2>
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Book ID</th>
            <th>Book Name</th>
            <th>Author</th>
            <th>Date Requested</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in acceptedBooks" :key="book.request_id">
            <td>{{ book.book_id }}</td>
            <td>{{ book.book_name }}</td>
            <td>{{ book.author }}</td>
            <td>{{ formatDate(book.date_requested) }}</td>
            <td>
              <button class="btn btn-outline-primary" @click="viewBook(book.book_id)">View</button>
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
    NavBar,
  },
  data() {
    return {
      acceptedBooks: [],
    };
  },
  mounted() {
    this.getAcceptedBooks();
  },
  methods: {
    getAcceptedBooks() {
      fetch('http://127.0.0.1:5000/mybooks', {
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
          this.acceptedBooks = data;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    viewBook(bookId) {
      this.$router.push(`/view-book/${bookId}`);
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
  },
};
</script>

<style scoped>
.table {
  margin-top: 20px;
}
</style>
