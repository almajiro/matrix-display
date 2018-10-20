<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="info">
      <b-navbar-brand href="#">Display Controller</b-navbar-brand>
    </b-navbar>
    <b-container fluid>
      <b-row class="input-messages">
        <b-col md="6" offset-md="3">
          <div class="cosmic">
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
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col md="6" offset-md="3">
          <div class="cosmic">
            <b-form-group
              label="1st Row Scroll Speed"
              label-for="message1-range"
            >
              <b-form-input v-model="message1_scroll_speed" type="range" id="message1-range" min="0"
                            max="100" class="speed-slider"></b-form-input>
            </b-form-group>
            <b-form-group
              label="2nd Row Scroll Speed"
              label-for="message1-range"
            >
              <b-form-input v-model="message2ScrollSpeed" type="range" id="message2-range" min="0"
                            max="100" class="speed-slider"></b-form-input>
            </b-form-group>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col md="6" offset-md="3">
          <div class="cosmic">
            <b-form-group
              label="1st Row Color"
            >
              <slider-picker v-model="colors" class="slider-picker"/>
              <material-picker v-model="colors" class="material-picker"/>
            </b-form-group>
            <b-form-group
              label="2nd Row Color"
            >
              <slider-picker v-model="colors" class="slider-picker"/>
              <material-picker v-model="colors" class="material-picker"/>
            </b-form-group>
            <div class="text-right">
              <b-button size="lg" variant="success" v-on:click="setSpeed">Save</b-button>
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <footer>
      <span>&copy; 2018 Kuroki Almajiro.</span>
    </footer>
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
    mounted() {
      axios
        .get(process.env.backendUrl + '/message/1').then(res => {
        this.message1 = res.data.payload.message
      })
      axios
        .get(process.env.backendUrl + '/message/2').then(res => {
        this.message2 = res.data.payload.message
      })
    },
    watch: {
      message1_scroll_speed: function () {
        this.setSpeed()
      }
    },
    methods: {
      setMessage: function () {
        axios
          .post(process.env.backendUrl + '/message/1', {message: this.message1}).then(res => {
          console.log(res.data)
        })
        axios
          .post(process.env.backendUrl + '/message/2', {message: this.message2}).then(res => {
          this.$swal({
            title: 'Message saved.',
            backdrop: false,
            type: 'success',
            background: 'rgb(61, 57, 126)',
            timer: 1500
          })
        })
      },
      setSpeed: function () {
        var payload = {speed: this.message1_scroll_speed}
        axios
          .post(process.env.backendUrl + '/message/1/speed', payload).then(res => {
          console.log(res.data)
          /*
          this.$swal({
            title: 'Scroll speed has been successfully changed.',
            backdrop: false,
            type: 'success',
            background: 'rgb(61, 57, 126)',
            timer: 1500
          })
          */
        })
      }
    }
  }
</script>

<style>
  body {
    color: #fff;
    background: rgb(47, 43, 105);
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
    --font-family-sans-serif: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
    --font-family-monospace: SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
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
    background-image: -webkit-gradient(linear, left top, right top, from(#00d9bf), to(#00d977));
    background-image: linear-gradient(to right, #00d9bf, #00d977);
    -webkit-box-shadow: 0 3px 0 0 #00bb85, 0 2px 8px 0 #00d99b, 0 4px 10px 0 rgba(33, 7, 77, .5);
    box-shadow: 0 3px 0 0 #00bb85, 0 2px 8px 0 #00d99b, 0 4px 10px 0 rgba(33, 7, 77, .5);
    border-radius: .5rem;
    text-shadow: 0 1px 3px rgba(0, 0, 0, .3);
    border: none;
    line-height: calc((1rem * 1.25) + 4px);
  }

  .btn-success:active {
    background-image: -webkit-gradient(linear, left top, right top, from(#00bba5), to(#0b6));
    background-image: linear-gradient(to right, #00bba5, #0b6);
    -webkit-box-shadow: none;
    box-shadow: none;
    border-color: transparent;
  }

  .navbar {
    margin-bottom: 10px;
    background-color: rgb(61, 57, 126) !important;
    height: 4.75rem;
    padding: 1.25rem;
  }

  .navbar-brand {
    padding: 0 1.25rem 0 0;
    font-size: 1.75rem;
    font-weight: 500;
    white-space: nowrap;
  }

  .messsage-input {
    margin-top: 10px !important;
  }

  .color-picker {

  }

  .slider-picker {
    width: 65% !important;
    float: right;
  }

  .material-picker {
    margin-left: 10px;
  }

  .vc-material {
    height: auto !important;
  }

  .cosmic {
    font-size: 1rem;
    line-height: 1.25;
    background: #3d3780;
    color: #d1d1ff;
    margin-bottom: 1.5rem;
    border-radius: .5rem;
    -webkit-box-shadow: 0 8px 20px 0 rgba(40, 37, 89, .6);
    box-shadow: 0 8px 20px 0 rgba(40, 37, 89, .6);
    font-weight: 400;
    border: 0 solid #3d3780;
    scrollbar-face-color: #554db3;
    scrollbar-track-color: #332e73;
    padding: 20px;
  }

  .speed-slider {
    -webkit-appearance: none;
    width: 100%;
    height: 20px;
    background: rgb(47, 43, 105);
    outline: none;
    opacity: 0.7;
    -webkit-transition: .2s;
    transition: opacity .2s;
  }

  footer {
    padding: 1.25rem;
    background: #3d3780;
    color: #a1a1e5;
    border-top: 1px solid #342e73;
  }

  .swal2-title {
    color: #fff !important;
  }
</style>
