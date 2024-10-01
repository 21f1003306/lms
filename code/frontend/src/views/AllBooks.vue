<template>
  <NavBar />
  <div class="container mt-5">
    <h2>Books</h2>
    <table class="table table-bordered table-hover">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in books" :key="book.id">
          <td>{{ book.id }}</td>
          <td>{{ book.name }}</td>
          <td>
            <div class="btn-group" role="group">
              <button v-if="role === 'admin'" class="btn btn-outline-primary" @click="updateBook(book.id)">Update</button>
              <button v-if="role === 'admin'" class="btn btn-outline-danger" @click="deleteBook(book.id)">Delete</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import userMixins from '../mixins/userMixins';
import NavBar from '../components/NavBar.vue';

export default {
  mixins: [userMixins],
  data() {
    return {
      books: [],
      role: '' // To store user role
    };
  },
  mounted() {
    this.getBooks();
    this.getUserRole(); // Fetch the user role
  },
  methods: {
    async getBooks() {
      fetch('http://127.0.0.1:5000/books', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        this.books = data.books;
      })
      .catch(error => {
        console.error('Error fetching books:', error);
      });
    },
    getUserRole() {
      fetch('http://127.0.0.1:5000/getuserinfo', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        this.role = data.role;
      })
      .catch(error => {
        console.error('Error fetching user info:', error);
      });
    },
    updateBook(bookId) {
      this.$router.push({ name: 'updatebook', params: { id: bookId } });
    },
    deleteBook(bookId) {
      fetch(`http://127.0.0.1:5000/book/${bookId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          'Content-Type': 'application/json',
        },
      })
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => { throw new Error(data.message || `HTTP error: ${response.status}`); });
        }
        return response.json();
      })
      .then(data => {
        alert(data.message);
        this.getBooks();  // Refresh the list of books after deletion
        this.$router.push('/allbooks');  // Redirect to the allbooks page
      })
      .catch(error => {
        alert(`Error deleting book: ${error.message}`);
        console.error(`Error deleting book with ID ${bookId}:`, error);
      });
    }
  }
};
</script>
