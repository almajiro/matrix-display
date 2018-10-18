<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="info">
        <b-navbar-brand href="#">Display Controller</b-navbar-brand>
      </b-navbar>
    <b-container fluid>
      <b-row class="input-messages">
        <b-col cols="6">
          <b-form-input v-model="message1" type="text" placeholder="Input your message"></b-form-input>
          <b-form-input v-model="message2" type="text" placeholder="Input your message"></b-form-input>
          <div class="text-right">
            <b-button size="lg" variant="success" v-on:click="setMessage">Save</b-button>
          </div>
        </b-col>
         <b-col class="preview-inputs">
           <p>Message1: {{ message1 }}</p>
          </b-col>
      </b-row>
    </b-container>
    <footer class="footer">
      <div class="container">
        <span class="text-muted">&copy; 2018 Kuroki Almajiro.</span>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  components: {},
  data () {
    return {
      message1: '',
      message2: ''
    }
  },
  methods: {
    setMessage: function (event) {
      var payload = {message: this.message1}
      axios
        .post('http://localhost:8080/message/1', payload).then(res => {
          console.log(res.data)
          this.$swal({title: 'Message saved.', backdrop: false, type: 'success', timer: 2000})
        })
    }
  }
}
</script>

<style>
  body {
    width: 100wh;
    height: 90vh;
    color: #fff;
    background: linear-gradient(-45deg, #EE7752, #E73C7E, #23A6D5, #23D5AB);
    background-size: 400% 400%;
    -webkit-animation: Gradient 15s ease infinite;
    -moz-animation: Gradient 15s ease infinite;
    animation: Gradient 15s ease infinite;
  }

  @-webkit-keyframes Gradient {
    0% {
      background-position: 0% 50%
    }
    50% {
      background-position: 100% 50%
    }
    100% {
      background-position: 0% 50%
    }
  }

  @-moz-keyframes Gradient {
    0% {
      background-position: 0% 50%
    }
    50% {
      background-position: 100% 50%
    }
    100% {
      background-position: 0% 50%
    }
  }

  @keyframes Gradient {
    0% {
      background-position: 0% 50%
    }
    50% {
      background-position: 100% 50%
    }
    100% {
      background-position: 0% 50%
    }
  }

  .form-control {
    background-color: rgba(1, 1, 1, 0.5);
    color: #fff;
  }

  .forn-control:focus {
    background-color: rgba(1, 1, 1, 0.5) !important;
    color: #fff !important;
  }

  .btn-success{
    color: #fff;
    background-color: #28a74575;
    border-color: #28a745;
    margin: 10px;
  }

  .navbar {
    margin-bottom: 10px;
    background-color: rgba(0,0,0,0.5) !important;
  }

  .footer {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 60px; /* Set the fixed height of the footer here */
    line-height: 60px; /* Vertically center the text there */
    background-color: #f5f5f5;
  }
</style>

