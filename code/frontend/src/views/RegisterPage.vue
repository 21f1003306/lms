<template>
    <NavBar />
    <div class="register-container">
        <form @submit.prevent="register">
            <h1>Register</h1>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" v-model="email" required />
            </div>
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" id="name" v-model="name" required />
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required />
            </div>
            <div class="mb-3">
                <label for="confirmPassword" class="form-label">Confirm Password</label>
                <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword" required />
            </div>
            <div class="mb-3">
                <label for="role" class="form-label">Role</label>
                <input type="text" class="form-control" id="role" v-model="role" required />
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            email: '',
            name: '',
            password: '',
            confirmPassword: '',
            role: ''
        };
    },
    methods: {
        async register() {
            // Check if passwords match
            if (this.password !== this.confirmPassword) {
                alert("Passwords do not match!");
                return;
            }

            try {
                const response = await fetch('http://localhost:5000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        name: this.name,
                        password: this.password,
                        role: this.role,
                    }),
                });
                const data = await response.json();
                console.log(data);
                if (response.ok) {
                    alert(data.message);
                    this.$router.push('/login');
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.log(error);
                alert("Some error occurred");
            }
        }
    }
};
</script>

<style scoped>
.register-container {
    margin: 50px;
}
</style>
