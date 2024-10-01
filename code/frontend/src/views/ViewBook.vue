<template>
  <NavBar />
  <div class="container mt-5">
    <h2>Book Details</h2>
    <div v-if="book" class="card">
      <div class="card-header">
        <h3>Book Name: {{ book.name }}</h3>
      </div>
      <div class="card-body d-flex">
        <div class="text-content">
          <p><strong>Author:</strong> {{ book.author }}</p>
          <p><strong>BookId:</strong> {{ book.id }}</p>
          <p><strong>Date Created:</strong> {{ formatDate(book.date_created) }}</p>
          <p><strong>Section:</strong> {{ sectionName }}</p>
          <p><strong>Content:</strong></p>
        </div>
        <div class="image-content">
          <img :src="`http://127.0.0.1:5000/images/${book.id}.png`" alt="Book Image" class="book-image" />
        </div>
      </div>
      <div class="card-body">
        <p><strong>PDF Content:</strong></p>
        <embed :src="`http://127.0.0.1:5000/content/${book.id}`" width="100%" height="600px" type="application/pdf">
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  data() {
    return {
      book: null,
      sectionName: '',
    };
  },
  mounted() {
    this.getBookDetails();
  },
  methods: {
    getBookDetails() {
      const bookId = this.$route.params.id;
      console.log('Book ID:', bookId); // Debugging line
      fetch(`http://127.0.0.1:5000/book/${bookId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        }
      })
      .then(response => {
        console.log('Response status:', response.status); // Debugging line
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Fetched data:', data); // Debugging line
        this.book = data.book;
        this.sectionName = data.section_name;
        this.book.content = 'this is the actual text'; // Assuming the actual content is here.
      })
      .catch(error => {
        console.error('Error fetching book details:', error);
        alert('Error fetching book details: ' + error.message);
      });
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    },
  }
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}

.card {
  margin-top: 20px;
}

.card-body.d-flex {
  display: flex;
  align-items: flex-start;
}

.text-content {
  flex: 1;
}

</style>
