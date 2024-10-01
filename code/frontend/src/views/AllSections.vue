<template>
    <NavBar />
    <div class="container mt-5">
      <h2>Sections</h2>
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="section in sections" :key="section.id">
            <td>{{ section.id }}</td>
            <td>{{ section.name }}</td>
            <td>
              <div class="btn-group" role="group">
                <button v-if="this.role == 'admin'" class="btn btn-outline-primary" @click="updateSection(section.id)">Update</button>
                <button v-if="this.role == 'admin'" class="btn btn-outline-danger" @click="deleteSection(section.id)">Delete</button>
                <router-link v-if="this.role == 'admin'" :to="`/add-books/${section.id}`">
                  <button class="btn btn-outline-success">Add Book</button>
                </router-link>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

  <script>
  import userMixins from '../mixins/userMixins'
  import NavBar from '../components/NavBar.vue'
  export default{
    mixins: [userMixins],
    data(){
        return{
            sections: [],
        };
    },
    mounted() {
        this.getSections();
        console.log("User role:", this.role);
    },
    methods: {
        getSections() {
            fetch('http://127.0.0.1:5000/sections', {
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
                this.sections = data.sections;
            })
            .catch(error => {
                console.error('Error:', error);
            })
        },
    updateSection(sectionId) {
      this.$router.push({ name: 'updatesection', params: { id: sectionId } });
    },
    deleteSection(sectionId) {
      fetch(`http://127.0.0.1:5000/section/${sectionId}`, {
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
        this.getSections();  // Refresh the list of section after deletion
        this.$router.push('/allsections');  // Redirect to the allsections page
      })
      .catch(error => {
        alert(`Error deleting section: ${error.message}`);
        console.error(`Error deleting section with ID ${sectionId}:`, error);
      });
    },
    }
  }
  </script>