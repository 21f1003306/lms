<template>
  <div>
    <NavBar />
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Book Name : {{ book.name }}</h3>
            </div>
            <div class="card-body">
              <h1>
                <p class="card-text blue-text">Please wait for the book request to be approved by Librarian.</p>
              </h1>
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
      book: {}, // Initialize book to an empty object
    };
  },
  mounted() {
    this.getBookDetails();
  },
  methods: {
    getBookDetails() {
      // Get book details from route params
      const bookId = this.$route.params.bookId;
      fetch(`http://127.0.0.1:5000/book/${bookId}`, {
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
          this.book = data.book;
        })
        .catch(error => {
          console.error('Error fetching book details:', error);
        });
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}
.blue-text {
  color: blue;
}
</style>
