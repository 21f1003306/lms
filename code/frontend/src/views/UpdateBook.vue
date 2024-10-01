<template>
  <NavBar />
  <div class="container mt-5">
    <div class="card">
      <div class="card-header">
        <h2>Update Book</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="updateBook" class="row g-3">
          <div class="col-md-6">
            <label for="bookName" class="form-label">Book Name:</label>
            <input v-model="bookName" type="text" class="form-control" id="bookName" required />
          </div>
          <div class="col-md-6">
            <label for="bookContent" class="form-label">Content:</label>
            <input v-model="bookContent" type="text" class="form-control" id="bookContent" required />
          </div>
          <div class="col-md-6">
            <label for="bookAuthor" class="form-label">Author:</label>
            <input v-model="bookAuthor" type="text" class="form-control" id="bookAuthor" required />
          </div>
          <div class="col-md-6">
            <label for="sectionDropdown" class="form-label">Section:</label>
            <select v-model="selectedSection" class="form-select" id="sectionDropdown" required>
              <option disabled value="">Select Section</option>
              <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
            </select>
          </div>
          <div class="col-12 mt-3">
            <button type="submit" class="btn btn-primary">Update Book</button>
          </div>
        </form>
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
      bookName: '',
      bookContent: '',
      bookAuthor: '',
      selectedSection: null,
      sections: [],
    };
  },
  created() {
    this.fetchSections();
    const bookId = this.$route.params.id;
    if (bookId) {
      this.fetchBookDetails(bookId);
    }
  },
  methods: {
    fetchSections() {
      fetch('http://127.0.0.1:5000/sections', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
        .then(response => response.json())
        .then(data => {
          this.sections = data.sections;
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
    fetchBookDetails(bookId) {
      fetch(`http://127.0.0.1:5000/book/${bookId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
        .then(response => response.json())
        .then(data => {
          this.bookName = data.book.name;
          this.bookContent = data.book.content;
          this.bookAuthor = data.book.author;
          this.selectedSection = data.book.section_id;
        })
        .catch(error => {
          console.error('Error fetching book details:', error);
        });
    },
    updateBook() {
      const bookId = this.$route.params.id;
      fetch(`http://127.0.0.1:5000/book/${bookId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
        body: JSON.stringify({
          name: this.bookName,
          content: this.bookContent,
          author: this.bookAuthor,
          section_id: this.selectedSection,
        }),
      })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          this.$router.push('/allbooks');
        })
        .catch(error => {
          console.error('Error updating book:', error);
        });
    },
  },
};
</script>

<style>
/* Add any specific styles for the UpdateBook component here */
</style>
