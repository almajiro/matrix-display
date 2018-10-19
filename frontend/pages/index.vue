<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="info">
      <b-navbar-brand href="#">Display Controller</b-navbar-brand>
      <b-nav-text right>&copy; 2018 Kuroki Almajiro.</b-nav-text>
    </b-navbar>
    <b-container fluid>
      <b-row class="input-messages">
        <b-col md="6">
          <b-form-group
            description="Please enter the character string you want to display on the first line."
            label="1st Row"
            label-for="message1"
          >
            <b-form-input v-model="message1" type="text" placeholder="Hello, " id="message1"></b-form-input>
          </b-form-group>
          <b-form-group
            description="Please enter the character string you want to display on the second line."
            label="2nd Row"
            label-for="message1"
          >
            <b-form-input v-model="message2" type="text" placeholder="World!"></b-form-input>
          </b-form-group>
          <div class="text-right">
            <b-button size="lg" variant="success" v-on:click="setMessage">Save</b-button>
          </div>
        </b-col>
        <b-col>
          <b-form-group
            label="1st Row Scroll Speed"
            label-for="message1-range"
          >
            <b-form-input v-model="message1_scroll_speed" type="range" id="message1-range" min="0"
                          max="10"></b-form-input>
          </b-form-group>
          <b-form-group
            label="2nd Row Scroll Speed"
            label-for="message1-range"
          >
            <b-form-input v-model="message2ScrollSpeed" type="range" id="message2-range" min="0"
                          max="10"></b-form-input>
          </b-form-group>
          <div class="text-right">
            <b-button size="lg" variant="success" v-on:click="setSpeed">Save</b-button>
          </div>
          <b-row>
            <b-col>
              <b-form-group
                label="1st Row Color"
              >
                <div class="color-picker">
                  <slider-picker v-model="colors"/>
                </div>
                <div class="color-picker">
                  <material-picker v-model="colors" class="material-picker" />
                </div>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group
                label="2nd Row Color"
              >
                <div class="color-picker">
                  <slider-picker v-model="colors"/>
                </div>
                <div class="color-picker">
                  <material-picker v-model="colors" class="material-picker" />
                </div>
              </b-form-group>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
  import axios from 'axios'
  import {Material, Slider} from 'vue-color'

  export default {
    components: {
      'material-picker': Material,
      'slider-picker': Slider
    },
    data() {
      return {
        message1: '',
        message2: '',
        colors: '#194d33',
        message1_scroll_speed: 4,
        message2ScrollSpeed: '',
      }
    },
    methods: {
      setMessage: function (event) {
        var payload = {message: this.message1}
        axios
          .post(process.env.backendUrl + '/message/1', payload).then(res => {
          console.log(res.data)
          this.$swal({title: 'Message saved.', backdrop: false, type: 'success', timer: 1000})
        })
      },
      setSpeed: function (event) {
        var payload = {speed: this.message1_scroll_speed}
        axios
          .post(process.env.backendUrl + '/message/1/speed', payload).then(res => {
          console.log(res.data)
          this.$swal({title: 'Scroll speed has been successfully changed.', backdrop: false, type: 'success', timer: 1000})
        })
      }
    }
  }
</script>

<style>
  body {
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

  .btn-success {
    color: #fff;
    background-color: #28a74575;
    border-color: #28a745;
  }

  .navbar {
    margin-bottom: 10px;
    background-color: rgba(0, 0, 0, 0.5) !important;
  }

  .messsage-input {
    margin-top: 10px !important;
  }

  .color-picker {
    float: left;
  }

  .material-picker {
    margin-left: 10px;
  }

  .vc-material {
    height: auto !important;
  }
</style>
