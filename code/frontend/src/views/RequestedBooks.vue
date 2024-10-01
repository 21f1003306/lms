<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <h2 v-if="user">{{ user.name }}'s Requested Books</h2>
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Book Id</th>
            <th>Book Name</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(request, index) in requestedBooks" :key="request.id">
            <td>{{ index + 1 }}</td>
            <td>{{ request.book_id }}</td>
            <td>{{ request.book_name }}</td>
            <td>{{ request.status }}</td>
            <td>
              <div class="btn-group" role="group">
                <button v-if="role === 'user' && request.status === 'accepted'" class="btn btn-outline-primary" @click="viewBook(request.book_id)">View</button>
                <button v-if="role === 'user' && request.status === 'accepted'" class="btn btn-outline-primary" @click="returnBook(request.id)">Return</button>
                <button v-if="role === 'user' && request.status === 'pending'" class="btn btn-outline-primary" @click="waitBook(request.book_id)">Waiting</button>

                <button v-if="role === 'user' && (request.status === 'returned')" class="btn btn-outline-danger" @click="Delete(request.id)">Delete Request</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import userMixins from '../mixins/userMixins';
import NavBar from '../components/NavBar.vue';

export default {
  mixins: [userMixins],
  components: {
    NavBar,
  },
  data() {
    return {
      requestedBooks: [],
    };
  },
  mounted() {
    this.getRequestedBooks();
  },
  methods: {
    getRequestedBooks() {
      fetch('http://127.0.0.1:5000/requests', {
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
          this.requestedBooks = data.requests;
        })
        .catch(error => {
          console.error('Error fetching requested books:', error);
        });
    },
    viewBook(bookId) {
      this.$router.push(`/view-book/${bookId}`);
    },
    waitBook(bookId) {
      this.$router.push({ name: 'waitbook', params: { bookId } });
    },
    returnBook(requestId) {
      fetch('http://127.0.0.1:5000/return-book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
        body: JSON.stringify({ request_id: requestId }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          console.log('Return book response:', data);
          if (data.message === 'Book returned successfully') {
            this.getRequestedBooks();
          } else {
            console.error('Unexpected response:', data);
          }
        })
        .catch(error => {
          console.error('Error returning book:', error);
        });
    },
    Delete(requestId) {
      fetch(`http://127.0.0.1:5000/delete-request`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
        body: JSON.stringify({ request_id: requestId }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          console.log(data);
          this.getRequestedBooks();
          alert(data.message);
        })
        .catch(error => {
          console.error('Error:', error);
        });
  },
  },
};
</script>

<style scoped>
.table {
  margin-top: 20px;
}
</style>
