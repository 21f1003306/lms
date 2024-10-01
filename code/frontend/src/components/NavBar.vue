<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/"><h4>My Library</h4></router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
                aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav">
                    <li v-if="!this.loggedin" class="nav-item">
                        <router-link class="nav-link" to="/login"><h5>Login</h5></router-link>
                    </li>
                    <li v-if="!this.loggedin" class="nav-item">
                        <a class="nav-link" href="#/register"><h5>Register</h5></a>
                    </li>
                    <li v-if="this.loggedin && (this.role=='user')" class="nav-item">
                        <router-link class="nav-link" to="/mybooks"><h5>My Books</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='user')" class="nav-item">
                        <router-link class="nav-link" to="/requested-books"><h5>Requested Books</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='user')" class="nav-item">
                        <router-link class="nav-link" to="/user-stat"><h5>User Statistics</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='user')" class="nav-item">
                        <router-link class="nav-link" to="/submit-feedback"><h5>Submit Feedback</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='user')" class="nav-item">
                        <router-link class="nav-link" to="/my-feedbacks"><h5>My Feedbacks</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='user')" class="nav-item">
                        <router-link class="nav-link" to="/my-profile"><h5>My Profile</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='user')" class="nav-item">
                        <router-link class="nav-link" to="/update-profile"><h5>Update Profile</h5></router-link>
                    </li>
                    
                    <li v-if="this.loggedin && (this.role=='admin')" class="nav-item">
                        <router-link class="nav-link" to="/createsection"><h5>Create Section</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='admin')" class="nav-item">
                        <router-link class="nav-link" to="/allsections"><h5>All Sections</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='admin')" class="nav-item">
                        <router-link class="nav-link" to="/allbooks"><h5>All Books</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='admin')" class="nav-item">
                        <router-link class="nav-link" to="/user-requests"><h5>User Requests</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='admin')" class="nav-item">
                        <router-link class="nav-link" to="/admin-stats"><h5>Admin Statistics</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='admin')" class="nav-item">
                        <router-link class="nav-link" to="/graph-stats"><h5>Graph</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='admin')" class="nav-item">
                        <router-link class="nav-link" to="/admin-feedback"><h5>User's Feedback</h5></router-link>
                    </li>
                    <li v-if="this.loggedin && (this.role=='admin')" class="nav-item">
                        <router-link class="nav-link" to="/all-users"><h5>All Users</h5></router-link>
                    </li>
                    <li v-if="this.loggedin" class="nav-item">
                        <a @click="logout" class="nav-link logout-link"><h5>Logout</h5></a>
                    </li>
                    <li v-if="this.loggedin && (this.role=='admin')" class="nav-item">
                        <a href="http://localhost:5000/download-book-requests" class="btn btn-dark mt-4">Download Report</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
import userMixins from '../mixins/userMixins'
export default {
    mixins: [userMixins]
}
</script>

<style scoped>
.logout-link {
    cursor: pointer;
}

.logout-link:hover {
    color: red;
    cursor: pointer;
}
</style>
