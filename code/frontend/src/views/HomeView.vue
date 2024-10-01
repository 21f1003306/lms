<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <h2 v-if="user" class="mb-4">{{ user.name }}'s Dashboard</h2>
      <h2 v-else class="mb-4">Please Login to Read Books</h2>
      <div class="mb-4" v-if="user">
        <label for="searchInput" class="me-2"><h4>Search Book:</h4></label>
        <input v-model="searchQuery" type="text" id="searchInput" class="form-control" @input="searchBooks" placeholder="Type a Book Name to search..." />
      </div>

      <!-- Alert Message -->
      <div v-if="alertMessage" class="alert alert-warning alert-dismissible fade show" role="alert">
        {{ alertMessage }}
        <button type="button" class="btn-close" @click="alertMessage = ''" aria-label="Close"></button>
      </div>

      <!-- Existing Section Handling -->
      <div v-for="section in sections" :key="section.id">
        <div v-if="section.visible !== false && section.books.length !== 0">
          <h2>{{ section.name }}</h2>
          <div class="row">
            <div v-for="book in section.books" :key="book.id" class="col-md-4 mb-4">
              <div v-if="book.visible !== false" class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h4>{{ book.name }}</h4>
                  <template v-if="user">
                    <router-link v-if="role === 'admin'" :to="'/view-book/' + book.id">View Book</router-link>
                    <button v-else-if="role === 'user'" @click="requestToRead(book)" class="btn btn-primary">Request to Read</button>
                  </template>
                </div>
                <div class="card-body">
                  <dl class="row">
                    <dt class="col-sm-4">Name:</dt>
                    <dd class="col-sm-8">{{ book.name }}</dd>
                    <dt class="col-sm-4">Author:</dt>
                    <dd class="col-sm-8">{{ book.author }}</dd>
                    <dt class="col-sm-4">Section:</dt>
                    <dd class="col-sm-8">{{ section.name }}</dd>
                    <dt class="col-sm-4">Book-Id:</dt>
                    <dd class="col-sm-8">{{ book.id }}</dd>
                    <dt class="col-sm-4">Image:</dt>
                    <dd class="col-sm-8"><img :src="`http://127.0.0.1:5000/images/${book.id}.png`" alt="Book Image" /></dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Books Section -->
    <div class="mb-4" v-if="showRecentBooks && recentBooks.length > 0">
      <h2>Most Recent Books</h2>
      <div class="row">
        <div v-for="book in recentBooks" :key="book.id" class="col-md-4 mb-4">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h4>{{ book.name }}</h4>
              <template v-if="user">
                <router-link v-if="role === 'admin'" :to="'/view-book/' + book.id">View Book</router-link>
                <button v-else-if="role === 'user'" @click="requestToRead(book)" class="btn btn-primary">Request to Read</button>
              </template>
            </div>
            <div class="card-body">
              <dl class="row">
                <dt class="col-sm-4">Name:</dt>
                <dd class="col-sm-8">{{ book.name }}</dd>
                <dt class="col-sm-4">Author:</dt>
                <dd class="col-sm-8">{{ book.author }}</dd>
                <dt class="col-sm-4">Section:</dt>
                <dd class="col-sm-8">{{ book.section }}</dd> 
                <dt class="col-sm-4">Book-Id:</dt>
                <dd class="col-sm-8">{{ book.id }}</dd>
                <dt class="col-sm-4">Image:</dt>
                <dd class="col-sm-8"><img :src="`http://127.0.0.1:5000/images/${book.id}.png`" alt="Book Image" /></dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import UserMixins from '../mixins/userMixins';

export default {
  components: {
    NavBar
  },
  mixins: [UserMixins],
  data() {
    return {
      sections: [],
      searchQuery: '',
      recentBooks: [],  // Data property for recent books
      showRecentBooks: true, // Data property to control visibility of recent books
      alertMessage: ''  // Data property for alert message
    };
  },
  mounted() {
    this.fetchSections();
    this.fetchRecentBooks();  // Fetch recent books on mount
  },
  methods: {
    fetchSections() {
      fetch('http://127.0.0.1:5000/sections', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response) => response.json())
      .then((data) => {
        this.sections = data.sections.map((section) => ({
          id: section.id,
          name: section.name,
          books: [],
        }));

        this.fetchBooksForSections();
      })
      .catch((error) => {
        console.error('Error fetching sections:', error);
      });
    },
    fetchBooksForSections() {
      this.sections.forEach((section) => {
        fetch(`http://127.0.0.1:5000/section/${section.id}/books`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        .then((response) => response.json())
        .then((data) => {
          section.books = data.books.map((book) => ({
            ...book,
            visible: true,
          }));
        })
        .catch((error) => {
          console.error(`Error fetching books for section ${section.name}:`, error);
        });
      });
    },
    fetchRecentBooks() {
      fetch('http://127.0.0.1:5000/most-recent-books', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response) => response.json())
      .then((data) => {
        this.recentBooks = data;  // Set recent books data
      })
      .catch((error) => {
        console.error('Error fetching recent books:', error);
      });
    },
    searchBooks() {
      const query = this.searchQuery.toLowerCase();

      this.sections.forEach((section) => {
        let sectionVisible = false;

        section.books.forEach((book) => {
          const bookName = book.name.toLowerCase();
          if (bookName.includes(query)) {
            book.visible = true;
            sectionVisible = true;
          } else {
            book.visible = false;
          }
        });

        section.visible = sectionVisible;
      });

      // Hide recent books section on search
      this.showRecentBooks = false;

      if (this.searchQuery === '') {
        // Show recent books section if the search query is cleared
        this.showRecentBooks = true;
      }
    },
    requestToRead(book) {
      const userId = this.user.id;
      const bookId = book.id;
      const bookName = book.name;

      fetch('http://127.0.0.1:5000/request-book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId, user_name: this.user.name, book_id: bookId, book_name: bookName }),
      })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
        alert(data.message);
        this.$router.push('/requested-books');
      })
      .catch((error) => {
        console.error('Error requesting book:', error);
      });
    }
  },
};
</script>

<style scoped>
.card {
  margin-top: 20px;
}
.float {
  position: fixed;
  width: 60px;
  height: 60px;
  bottom: 70px;
  right: 70px;
  background-color: #0C9;
  color: #FFF;
  border-radius: 50px;
  text-align: center;
  box-shadow: 2px 2px 3px #999;
}
.my-float {
  margin-top: 15px;
}
</style>
