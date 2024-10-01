<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <h2>Submit Feedback</h2>
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card p-4">
            <div v-if="role === 'user'">
              <!-- Book Selection -->
              <div class="mb-3">
                <label for="book" class="form-label"><h5>Book</h5></label>
                <select class="form-select" v-model="book_id" required>
                  <option v-for="book in filteredBooks" :key="book.id" :value="book.id">
                    {{ book.name }}
                  </option>
                </select>
              </div>

              <!-- Rating -->
              <div class="form-group">
                <label for="rating"><h5>Rating:</h5></label>
                <div class="rating-strip">
                  <span
                    v-for="star in stars"
                    :key="star"
                    @click="setRating(star)"
                    :class="{
                      selected: star <= Math.floor(rating),
                      half: star === Math.ceil(rating) && rating % 1 > 0,
                      hover: star <= hoverRating
                    }"
                    @mouseover="hoverRating = star"
                    @mouseleave="hoverRating = 0"
                  >
                    ★
                  </span>
                </div>
              </div>

              <!-- Comment -->
              <div class="mb-3">
                <label for="comment" class="form-label"><h5>Comment</h5></label>
                <textarea v-model="comment" id="comment" class="form-control" required></textarea>
              </div>

              <button @click="submitFeedback" class="btn btn-primary">Submit Feedback</button>
            </div>
            <p v-if="successMessage" class="text-success mt-3">{{ successMessage }}</p>
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
    NavBar
  },
  mixins: [UserMixins],
  data() {
    return {
      books: [],
      bookRequests: [],
      stars: [1, 2, 3, 4, 5],
      rating: 0,
      hoverRating: 0,
      comment: '',
      book_id: '',
      successMessage: ''
    };
  },
  computed: {
    filteredBooks() {
      // Filter books based on requests' status being 'accepted'
      return this.books.filter(book => 
        this.bookRequests.some(request => request.book_id === book.id && request.status === 'accepted')
      );
    }
  },
  mounted() {
    this.fetchBooks();
    this.fetchBookRequests();
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await fetch('http://127.0.0.1:5000/books', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          },
        });
        const data = await response.json();
        console.log('Books fetched:', data.books); // Debugging output
        this.books = data.books;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    async fetchBookRequests() {
      try {
        const response = await fetch('http://127.0.0.1:5000/requests', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          },
        });
        const data = await response.json();
        console.log('Book requests fetched:', data.requests); // Debugging output
        this.bookRequests = data.requests;
      } catch (error) {
        console.error('Error fetching book requests:', error);
      }
    },
    setRating(star) {
      this.rating = star;
    },
    submitFeedback() {
      const userId = this.user.id;
      const userName = this.user.name;
      const selectedBook = this.books.find(book => book.id === parseInt(this.book_id));
      const bookName = selectedBook ? selectedBook.name : '';
      const comment = this.comment;
      const rating = this.rating;

      fetch('http://127.0.0.1:5000/submit-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          user_name: userName,
          book_id: this.book_id,
          book_name: bookName,
          comment: comment,
          rating: rating
        }),
      })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
        alert(data.message);
        this.$router.push('/my-feedbacks');
      })
      .catch((error) => {
        console.error('Error submitting feedback:', error);
      });
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 1500px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-top: 20px;
}
.rating-strip {
  display: justify;
  font-size: 4rem;
  cursor: pointer;
  color: grey;
}
.rating-strip span.selected {
  color: #007bff; /* Color for selected stars */
}
</style>
