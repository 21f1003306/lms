<template>
 <NavBar/>
    <div class="container mt-5">
      <h2>Create Section</h2>
      <form @submit.prevent="createSection" class="mt-3">
        <div class="mb-3">
          <label for="sectionName" class="form-label">Section Name</label>
          <input v-model="sectionName" type="text" class="form-control" id="sectionName" required>
        </div>
        <div class="mb-3">
          <label for="sectionDescription" class="form-label">Section Description</label>
          <input v-model="sectionDescription" type="text" class="form-control" id="sectionDescription" required>
        </div>
        <button type="submit" class="btn btn-primary">Create Section</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        sectionName: '',
        sectionDescription: '',
      };
    },
    methods: {
      async createSection() {
        try {
          const response = await fetch('http://localhost:5000/section', {
            method: 'POST',
            headers: {
              'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              name: this.sectionName,
              description: this.sectionDescription,
            }),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            alert(data.message);
            this.$router.push('/allsections');
            // Route to all sections
          } else {
            alert('Error: ' + data.error);
          }
        } catch (error) {
          console.error('Create section error:', error);
          alert('An error occurred while creating the section.');
        }
      },
    },
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>