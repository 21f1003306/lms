<template>
  <div>
    <NavBar/>
    <div class="container mt-5">
      <h2>All User's Requests</h2>
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Book Id</th>
            <th>Book Name</th>
            <th>User Id</th>
            <th>User Name</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requestedBooks" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.book_id }}</td>
            <td>{{ request.book_name }}</td>
            <td>{{ request.user_id }}</td>
            <td>{{ request.user_name }}</td>
            <td>{{ request.status }}</td>
            <td>
              <div class="btn-group" role="group">
                <button v-if="role === 'admin' && request.status === 'pending'" class="btn btn-outline-primary" @click="Accept(request.id)">Accept</button>
                <button v-if="role === 'admin' && request.status === 'pending'" class="btn btn-outline-primary" @click="Reject(request.id)">Reject</button>
                <button v-if="role === 'admin' && request.status === 'accepted'" class="btn btn-outline-primary" @click="Revoke(request.id)">Revoke</button>
                
                <button v-if="role === 'admin' && (request.status === 'revoked' || request.status === 'rejected')" class="btn btn-outline-danger" @click="Delete(request.id)">Delete Request</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import UserMixins from '../mixins/userMixins';

export default {
  mixins: [UserMixins],
  components: {
    NavBar
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
      fetch('http://127.0.0.1:5000/user-requests', {
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
          console.error('Error:', error);
        });
    },
    Accept(requestId) {
      fetch(`http://127.0.0.1:5000/accept-request`, {
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
          alert('Request accepted successfully');
          this.getRequestedBooks();
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    Reject(requestId) {
  fetch('http://127.0.0.1:5000/reject-request', {
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
  })
  .catch(error => {
    console.error('Error:', error);
  });
},  
    Revoke(requestId) {
      fetch(`http://127.0.0.1:5000/revoke-request`, {
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
        })
        .catch(error => {
          console.error('Error:', error);
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
