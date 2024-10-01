<template>
  <NavBar />
  <div class="container mt-5">
    <div class="card">
      <div class="card-header">
        <h2>Add Book</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="addBook" class="row g-3">
          <div class="col-md-6">
            <label for="bookName" class="form-label">Book Name:</label>
            <input v-model="bookName" type="text" class="form-control" id="bookName" required />
          </div>
          <div class="col-md-6">
            <label for="bookContent" class="form-label">Content:</label>
            <input type="file" class="form-control" id="bookContent" @change="addPdf" />
          </div>
          <div class="col-md-6">
            <label for="bookAuthor" class="form-label">Author:</label>
            <input v-model="bookAuthor" type="text" class="form-control" id="bookAuthor" required />
          </div>
          <div class="col-md-6">
            <label for="bookImage" class="form-label">Book Image:</label>
            <input type="file" class="form-control" id="bookImage" @change="addFile" />
          </div>
          <div class="col-md-6">
            <label for="sectionDropdown" class="form-label">Section:</label>
            <select v-model="selectedSection" class="form-select" id="sectionDropdown" required>
              <option disabled value="">Select Section</option>
              <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
            </select>
          </div>
          <div class="col-12 mt-3">
            <button type="submit" class="btn btn-primary">Add Book</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bookName: '',
      bookContent: null,
      bookAuthor: '',
      bookImage: null,
      selectedSection: null,
      sections: [],
    };
  },
  created() {
    this.fetchSections();
    const sectionIdFromRoute = this.$route.params.id;
    if (sectionIdFromRoute) {
      this.selectedSection = sectionIdFromRoute;
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
    addFile(event) {
      this.bookImage = event.target.files[0];
      console.log(this.bookImage,"image")
    },
    addPdf(event) {
      this.bookContent = event.target.files[0];
            console.log(this.bookContent,"content")

    },
    addBook() {
      const formData = new FormData();
      formData.append('name', this.bookName);
      formData.append('book_content', this.bookContent);
      formData.append('author', this.bookAuthor);
      formData.append('section_id', this.selectedSection);
      if (this.bookImage) {
        formData.append('book_image', this.bookImage);
      }

      fetch(`http://127.0.0.1:5000/section/${this.selectedSection}/add-book`, {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
        body: formData
      })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          this.$router.push('/allbooks');
        })
        .catch(error => {
          console.error('Error adding book:', error);
        });
    },
  },
};
</script>

<style>
.container {
  margin-top: 20px;
}
.card {
  margin-top: 20px;
}
</style>
