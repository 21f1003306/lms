<template>
  <NavBar />
  <div class="container mt-5">
    <div class="card">
      <div class="card-header">
        <h2>Update Section</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="updateSection" class="row g-3">
          <div class="col-md-6">
            <label for="sectionName" class="form-label">Section Name:</label>
            <input v-model="sectionName" type="text" class="form-control" id="sectionName" required />
          </div>
          <div class="col-md-6">
            <label for="sectionDescription" class="form-label">Description:</label>
            <input v-model="sectionDescription" type="text" class="form-control" id="sectionDescription" required />
          </div>
          <div class="col-12 mt-3">
            <button type="submit" class="btn btn-primary">Update Section</button>
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
      sectionName: '',
      sectionDescription: '',
    };
  },
  created() {
    const sectionId = this.$route.params.id;
    if (sectionId) {
      this.fetchSectionDetails(sectionId);
    }
  },
  methods: {
    fetchSectionDetails(sectionId) {
  fetch(`http://127.0.0.1:5000/section/${sectionId}`, {
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
      if (!data.section_data) {
        throw new Error('Section data not found');
      }
      this.sectionName = data.section_data.name;
      this.sectionDescription = data.section_data.description;
    })
    .catch(error => {
      console.error('Error fetching section details:', error);
      alert('Error fetching section details: ' + error.message);
    });
},


    updateSection() {
      const sectionId = this.$route.params.id;
      fetch(`http://127.0.0.1:5000/section/${sectionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
        body: JSON.stringify({
          name: this.sectionName,
          description: this.sectionDescription,
        }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          alert(data.message);
          this.$router.push('/allsections');
        })
        .catch(error => {
          console.error('Error updating section:', error);
          alert('Error updating section: ' + error.message);
        });
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}

.card {
  margin-top: 20px;
}
</style>

