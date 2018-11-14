<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="info">
      <b-navbar-brand href="#">RGB Matrix Display Controller</b-navbar-brand>
    </b-navbar>
    <b-container fluid>
      <b-row class="input-messages">
        <b-col md="6" offset-md="3">
          <div class="cosmic">
            <b-form-group
              description="1行目に表示したい文字列を入力してください。"
              label="1行目">
              <b-form-input v-model="message[0]" type="text" placeholder="Hello, " v-on:change="setMessage(1)"></b-form-input>
            </b-form-group>
            <div class="text-center">
              <b-button size='sm' variant='success' v-on:click="setMode(1)">この行のみを表示</b-button>
            </div>
            <b-form-group
              description="2行目に表示したい文字列を入力してください。"
              label="2行目">
              <b-form-input v-model="message[1]" type="text" placeholder="World!" v-on:change="setMessage(2)"></b-form-input>
            </b-form-group>
            <div class="text-center">
              <b-button size='sm' variant='success' v-on:click="setMode(2)">この行のみを表示</b-button>
            </div>
            <div class="text-center show-all">
              <b-button size='sm' variant='success' v-on:click="showAll()">全てを表示</b-button>
            </div>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col md="6" offset-md="3">
          <div class="cosmic">
            <b-form-group
              label="1行目 スクロール速度"
              label-for="message1-range"
            >
              <b-form-input v-model="message_scroll_speed[0]" type="range" id="message1-range" min="0"
                            max="20" class="speed-slider" v-on:change="setSpeed(1)"></b-form-input>
            </b-form-group>
            <b-form-group
              label="2行目 スクロール速度"
              label-for="message1-range"
            >
              <b-form-input v-model="message_scroll_speed[1]" type="range" id="message2-range" min="0"
                            max="20" class="speed-slider" v-on:change="setSpeed(2)"></b-form-input>
            </b-form-group>
          </div>
        </b-col>
      </b-row>
      <no-ssr>
        <b-row>
          <b-col md="6" offset-md="3">
            <div class="cosmic">
              <b-form-group
                label="1行目 文字色"
              >
                <slider-picker v-model="message_color[0]" class="slider-picker" @input="setColor(1)"/>
                <material-picker v-model="message_color[0]" class="material-picker" @input="setColor(1)"/>
                <div class="text-center show-all">
                  <b-button size='sm' variant='success' v-on:click="setRainbow(1)">Rainbow / 単色</b-button>
                </div>
              </b-form-group>
              <b-form-group
                label="2行目 文字色"
              >
                <slider-picker v-model="message_color[1]" class="slider-picker" @input="setColor(2)"/>
                <material-picker v-model="message_color[1]" class="material-picker" @input="setColor(2)"/>
                <div class="text-center show-all">
                  <b-button size='sm' variant='success' v-on:click="setRainbow(2)">Rainbow / 単色</b-button>
                </div>
              </b-form-group>
            </div>
          </b-col>
        </b-row>
      </no-ssr>
    </b-container>
    <footer>
      <span>&copy; 2018 <a href="http://www.almajiro.tokyo" class="creator">Kuroki Almajiro</a>.</span>
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
        message: ['', ''],
        show: [0, 0],
        rainbow: [0, 0],
        message_color: [
          { r: 255, g: 0, b: 0 },
          { r: 255, g: 0, b: 0 }
        ],
        message_scroll_speed: [4, 4],
      }
    },
    created() {
      axios
        .get(process.env.backendUrl + '/message/1').then(res => {
        this.message[0] = res.data.payload.message
      })
      axios
        .get(process.env.backendUrl + '/message/2').then(res => {
        this.message[1] = res.data.payload.message
      })
      axios
        .get(process.env.backendUrl + '/message/1/speed').then(res => {
        this.message_scroll_speed[0] = res.data.payload.speed
      })
      axios
        .get(process.env.backendUrl + '/message/2/speed').then(res => {
        this.message_scroll_speed[1] = res.data.payload.speed
      })
    },
    methods: {
      setMessage: function (row) {
        axios.post(process.env.backendUrl + '/message/' + row, {message: this.message[row-1]}).then(res => {

        })
      },
      setSpeed: function (row) {
        axios
          .post(process.env.backendUrl + '/message/' + row +'/speed', {speed: this.message_scroll_speed[row-1]})
          .then(res => {

          })
      },
      setColor: function (row) {
        let payload = {
          colors: {
            red: this.message_color[row -1].rgba.r,
            green: this.message_color[row -1].rgba.g,
            blue: this.message_color[row -1].rgba.b,
          }
        }
        axios.post(process.env.backendUrl + '/message/' + row + '/color', payload).then(res => {
          
        })
      },
      setMode: function (row) {
        axios.post(process.env.backendUrl + '/row/' + row).then(res => {
          
        })
      },
      showAll: function () {
        axios.post(process.env.backendUrl + '/mode', {mode: false}).then(res => {
          
        })
      },
      setRainbow: function (row) {
        axios.post(process.env.backendUrl + '/mode', {rainbow: !this.rainbow[row-1]}).then(res => {
          
        })
      }
    }
  }
</script>

<style>
  body {
    color: #fff;
    background: rgb(47, 43, 105);
  }

  .creator {
    color: #a1a1e5;
  }

  .creator:hover {
    color: #a1a1e5;
    text-decoration: none;
  }

  .form-control {
    padding: .75rem 1.125rem;
    color: #fff;
    background-color: #37317a;
    border: 2px solid #342e73;
    border-radius: .5rem;
  }

  .form-control:focus {
    border: 2px solid #7659ff;
    background-color: #342e73;
    -webkit-box-shadow: none;
    box-shadow: none;
    color: #fff;
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

  .slider-picker {
    width: 65% !important;
    float: right;
  }

  .material-picker {
    margin-left: 10px;
    width: 30% !important;
    border-radius: 10px !important;
  }

  .vc-slider-swatch-picker {
    border-radius: 5px !important;
  }

  .vc-material {
    height: auto !important;
    width: 100%;
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
    direction: rtl;
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

  .show-all {
    padding-top: 15px;
  }
</style>
