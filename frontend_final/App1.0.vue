<template>
  <div id="app">
    <div class="home col" >
      <section class="first row">
	  <div>
          <p class="logoText">My Perfect Recipe</p>
          <p class="logoText2">—— Best suits your needs ——</p>
        </div>
		</section>
	<section class="second col">
        <div class="searchbar" :class="{'fix':searchBarFixed}">
          <el-autocomplete
            class="search"
            v-model="inputValue"
            :fetch-suggestions="querySearch"
            placeholder="please input your ingredient"
            @select="handleSelect"
          >
            <!--这里是搜索框的内容-->
            <!--select这里会显示所选的内容-->
            <el-button slot="append" icon="el-icon-search" @click="handleSearchClick"></el-button>
            <!--          按下回车键既可以进行搜索-->
          </el-autocomplete>
          <section class="checkbox-area row">
            <el-checkbox-group v-model="checkGroup">
              <el-checkbox label="Very Hungry" style="color:white" ></el-checkbox>
              <el-checkbox label="I Can Go Shopping" style="color:white"></el-checkbox>
            </el-checkbox-group>
          </section>
        </div>
        <div :class="{'blank':searchBarFixed}"></div>

<!--        <section>
          <div>
            <transition name="fade">
              <loading v-if="isLoading"></loading>
            </transition>
          </div>
        </section>-->

        <section class="collapse-area">
          <div class="triangle" @click="foldAll">
            <div class="triangle-item" :class="{'rotate':isCollapse}"></div>
            <span style="margin-left:15px;" class="text-color">Select What You Have</span>
          </div>
          <el-collapse
            v-model="activeNames"
            @change="handleChange"
            v-if="isCollapse"
            class="collapse-panel"
          >
            <el-collapse-item :name="index" v-for="(item,index) in checkData" :key="index">
              <p style="margin-left:15px;" slot="title" >
                <el-icon
                  class="el-icon-arrow-right"
                  :class="{'rotate':activeNames.includes(index)}"
                ></el-icon>
                {{item.title}}
              </p>
              <el-row>
                <el-col :span="4" v-for="(sub,key) in item.check" :key="key" style="text-align:left ; margin-left: 170px">
                  <el-checkbox :label="sub" @change="handleAddCheck(sub)"></el-checkbox>
                </el-col>
              </el-row>
            </el-collapse-item>
          </el-collapse>
          <!-- loading区域 -->
          <div class="loading" style="width:100%;height:30px"
            v-loading="loading"
            :element-loading-text="loading_text"
            element-loading-spinner="el-icon-loading"
            element-loading-background="rgba(0, 0, 0, 0.8)"
          >
          <p v-if="loading">{{ loading_text }}</p>
          <p v-if="message.length" style="margin-left:25px;" class="text-color">{{message}}</p>
		  <p v-if="refresh_message.length" style="margin-left:25px;" class="text-color">{{refresh_message}}</p>
		  </div>
        </section>
      </section>
      <!-- 图片展示区域 -->
      <section class="third col">
        <transition name="el-fade-in-linear">
          <el-row v-show="imgs.length" class="img-container" :gutter="10">
            <el-col  v-for="(item,index) in imgs" :key="index" :span="8">
              <div
              class="img-item"
              @mouseover="() => handleImageHover(item)"
              @mouseout="() => handleImageOut(item)"
            >
              <el-image :src="item.src" fit="fill">
                <div slot="placeholder" class="image-slot">
                  <!-- loading<span class="dot">...</span> -->
                  <!--                  <span v-for="desc in item.desc" :key="desc">{{desc}}</span>-->
                </div>
                <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
              <div
                class="img-hover-info"
                v-show="item.isHover"
                @click="() => handleJumpClick(item)"
              >
                <div class="title">{{item.title}}</div>
                <div class="desc">{{item.desc}}</div>
                <!--                <span v-for="desc in item.desc" :key="desc">{{desc}}</span>-->
              </div>
            </div>
            </el-col>
          </el-row>
          <!-- <div class="img-contaienr row" v-show="imgs.length">
            <div
              class="img-item"
              v-for="item in imgs"
              :key="item.id"
              @mouseover="() => handleImageHover(item)"
              @mouseout="() => handleImageOut(item)"
            >
              <el-image :src="item.src" fit="fill">
                <div slot="placeholder" class="image-slot">
                </div>
                <div slot="error" class="image-slot">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
              <div
                class="img-hover-info"
                v-show="item.isHover"
                @click="() => handleJumpClick(item)"
              >
                <div class="title">{{item.title}}</div>
                <div class="desc">{{item.desc}}</div>
              </div>
            </div>
          </div> -->
        </transition>
        <el-button class="footer-btn" icon="el-icon-arrow-down" circle @click="refreshClick"></el-button>
        <back-to-top></back-to-top>
      </section>
    </div>
  </div>
</template>

<script>
  import DataList from "./assets/dataList.js";
  import BackToTop from "./components/backToTop";
  const testData1 = [
    {
      url: "http://www.baidu.com",
      id: 1,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      title: "title",
      desc: "hi testdata1"
    },
    {
      url: "",
      id: 2,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      title: "",
      desc: "图片描述"
    },
    {
      url: "",
      id: 3,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      title: "",
      desc: "图片描述"
    },
    {
      url: "",
      id: 4,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      title: "",
      desc: "图片描述"
    },
    {
      url: "",
      id: 5,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      title: "",
      desc: "图片描述"
    },
    {
      url: "",
      id: 6,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      title: "",
      desc: "图片描述"
    },
    {
      url: "",
      id: 7,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      title: "",
      desc: "图片描述"
    },
    {
      url: "",
      id: 8,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      title: "",
      desc: "图片描述"
    },
    {
      url: "",
      id: 9,
      src:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
      title: "",
      desc: "图片描述"
    }
  ];
  const testData2 = [
    {
      id: 1,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "hi testdata 2"
    },
    {
      id: 2,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 3,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 4,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 5,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 6,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 7,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 8,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    },
    {
      id: 9,
      src:
          "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
      desc: "图片描述2"
    }
  ];
  const tempFlag = {
    search: true,
    refresh: true
  };
  // @ is an alias to /src
  import axios from "axios";
  export default {
    name: "home",
    components: { BackToTop },
    data() {
      return {
        searchBarFixed:false,
      isCollapse: false,
      imgs: [],
		//added part
		recipe_ids: [],
		length_recipe_ids : "",
		recipe_idslist:[],
		counter : 0,
		check_imgs : [],
		temperature : "",
		status : "",
		future_status : "",
		error: false,
		message: "",
		mounted_imgsids:[],
		loading: false,
		refresh_button:true,
		refresh_message:"",
		//end added part
        inputValue: "",
      activeNames: [0],
      selectCheck: [],
      checkData: DataList.checkBox,
      checkList: [],
      checkGroup: [],
      loading_text: 'Fetching fresh and delicious recipes from our huge recipes farm. Please wait'
      };
    },
    computed: {
      isRotate() {
        // var index = this.activeNames.indexOf("0");
        if (this.activeNames.length > 0) {
          return true;
        } else {
          return false;
        }
      },
	},
    async mounted() {
      //this.getData();
      this.imgs = [];
	  try{
	  const response= await axios.get('http://127.0.0.1:5000/getip'); 
		//data = JSON.parse(data);
		console.log(response.data);
		//if (response.data.weather==0){
			this.recipe_ids = response.data.recipe_info;
			this.mounted_imgsids = this.recipe_ids;
			this.message = response.data.message;
			this.length_recipe_ids = response.data.length;
			await this.retrieveData(1);
			this.imgs = this.check_imgs;
		//}else{
		//this.imgs[0].desc = response.data.recipe_info+" "+response.data.temp+" "+response.data.present_status+"\n"+response.data.future_status;
		//this.temperature = response.data.temp;
		//this.status = response.data.present_status;
		//this.future_status = response.data.future_status;
		//}
		}
		catch(error){
				console.error(error);
				this.imgs[0].desc = 'error';
			}
	
      window.addEventListener("scroll", this.handleScroll, true);
    },
    destroyed() {
      window.removeEventListener("scroll", this.handleScroll, true);
    },
    methods: {
      //监听页面下滚150px
      handleJumpClick(item) {
        // window.location.href = item.url  在原有标签打开超链接
        window.open(item.url)
      },
	  handleScroll(e) {
      let scrollTop =
        window.pageYOffset ||
        document.documentElement.scrollTop ||
        document.body.scrollTop;
      let offsetTop = document.querySelector(".second").offsetTop;
      console.log(`scrlltop:${scrollTop}=====offsettop${offsetTop}`)
      scrollTop > offsetTop
        ? (this.searchBarFixed = true)
        : (this.searchBarFixed = false);
      //  页面一旦滑动一段距离，就弹出悬浮搜索框
    },
      handleAddCheck(value) {
        var index = this.selectCheck.indexOf(value);
        if (index >= 0) {
          this.selectCheck.splice(index, 1);
        } else {
          this.selectCheck.push(value);
        }
      },
	  async retrieveData(status){
	  //var recipe_idslist = [];
	  if(status==1){
		this.counter = 0;
		if (this.length_recipe_ids == '0'){
		this.check_imgs = this.mounted_imgsids;
		return ;
	  }
	  }
	  
	  var local_counter = this.counter+9;
	  var recipe_idslist =[];
	  while(this.counter<local_counter){
			if(this.counter <this.length_recipe_ids){
		recipe_idslist.push(this.recipe_ids[this.counter]);
		this.counter++;
		}
		else{

		this.refresh_button = false;
		this.refresh_message = this.counter+" "+this.length_recipe_ids;
		this.check_imgs = [];
		if(this.recipe_idslist.length){
			break;
		}
		return ;
		}
	  }
	  
	  recipe_idslist = recipe_idslist.toString();
	  
	  try{
	  const response = await axios.get("http://127.0.0.1:5000/retrieve", {params: {recipe_list:recipe_idslist,city:this.place,latitude:this.latitude,longitude:this.longitude}});
	  //.then((response) => {
		//let res = response.data;
		console.log(response.data);
		this.check_imgs = [];
		this.check_imgs = response.data.recipe_info;
	  //})
	  }catch(error){
				console.error(error);
		}
		
	  //var imgs_length = this.check_imgs.length;
	  //var i = 0;
	  //while(imgs_length < 9){
		//	this,check_imgs.push(testData1[i]);
			//i++;
			//imgs_length++;
		//}
		//this.imgs = this.check_imgs;
		//this.recipe_idslist = [];
	  },
      async getData() {
		try{
			this.message = "";
			this.loading = true;
         const response = await axios.get("http://127.0.0.1:5000/test", {
              // 传递参数
              params: {
                city: this.inputValue,
				shopping_hungry: this.checkGroup.toString(),
				checkbox: this.selectCheck.toString(),
              }
            });
            //.then((response) => {
              // 请求成功
              //let res = response.data;
         console.log(response.data);
              //这个res就是请求回来的数据，可以在控制台看到，下面是修改了一条图片描述
              this.recipe_ids = response.data.id;
			  this.length_recipe_ids = response.data.length;
			  
			  //this.error = (response.data.error == 1 || response.data.error ==2);
			  
			  if(response.data.error==1){
			  this.recipe_ids = this.mounted_imgsids;
			  this.length_recipe_ids = this.mounted_imgsids.length;
			  }
				
			  await this.retrieveData(1);
			  this.loading = false;
			  this.message = response.data.message;
              //this.imgs[0].desc = res.data;
            //})
			}catch(error){
			this.error = error;
				console.error(error);
			}
	  },
      //每次取的时候先写个函数去修改它的key，image1=image+'1'这样
	
      async handleSearchClick() {
		this.error = false;
		this.refresh_button = true;
				this.refresh_message = "";
        await this.getData();
		//this.imgs[0].desc=this.check_imgs[0].desc;
		//this.retrieveData();
        //tempFlag.refresh = !tempFlag.refresh;
		
		this.imgs = this.check_imgs;
		this.check_imgs = [];
		this.imgs[0].desc = this.length_recipe_ids;
		this.imgs[1].desc = this.error;
		//this.imgs[0].desc = this.recipe_idslist;
		//this.imgs[0].desc = this.res.data;
      },
      async refreshClick() {
		await this.retrieveData(0);
        //tempFlag.search = !tempFlag.search;
        const arr = this.imgs.concat(this.check_imgs);
        this.imgs = arr;

		this.imgs[1].desc = this.length_recipe_ids+" "+this.counter;
      },
      handleImageHover(item) {
      this.$set(item, "isHover", true);
    },
    handleImageOut(item) {
      this.$set(item, "isHover", false);
    },
    querySearch(queryString, cb) {
      var checkList = this.checkList.map(item => ({ value: item }));
      var results = queryString
        ? checkList.filter(this.createFilter(queryString))
        : checkList;
      cb(results);
    },
    createFilter(queryString) {
      return checkList => {
        return (
          checkList.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
        );
      };
    },
    handleSelect(item) {
      console.log(item);
    },
    handleChange() {},
    foldAll() {
      if (this.isCollapse) {
        this.activeNames = [];
        this.isCollapse = false;
      } else {
        this.isCollapse = true;
        this.activeNames = [0];
      }
    }
  }
};
</script>

<style lang="less" scoped>
html {
  padding: 0px;
  margin: 0px;
} /*这是把白边去掉的方法*/
html,
#app::-webkit-scrollbar {
  display: none;
}
#app {
  font-family: "calibri", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
/*.isScroll {
    background: linear-gradient(
            to right,
            rgba(30, 87, 153, 0.8) 0%,
            rgba(30, 87, 153, 0.8) 44%,
            rgba(41, 137, 216, 0.8) 94%
    ) !important; !* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ *!
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#cc1e5799', endColorstr='#cc2989d8',GradientType=1 );
  }*/
.col {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.row {
  display: flex;
  flex-flow: row wrap;
  justify-content: center;
  align-items: center;
}
.home {
  //背景
  width: 100%;
  width: 100%;
  background: black;
  /*background: url('https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg');*/
  /*用url设置背景图*/
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: 100% 100%;
  /*最底层页面*/
  .first {
    position: relative;
    top: 0;
    z-index: 100;
    width: 100%;
    height: 500px;
    background-image: url("https://s3-us-west-2.amazonaws.com/lightstalking-assets/wp-content/uploads/2019/10/29111706/photo-by-hans-vivek-1024x576.jpg");
    background-repeat: no-repeat;
    background-size: 100% 100%;
    
  }
  .shadow {
    box-shadow: 1px 1px 3px black;
    /*background: url("./assets/fast-food.jpg");*/
    /*background-color: red !important;*/
    /*background-image: linear-gradient(180deg, white 19%, black 80%) !important;*/
    /*  悬浮搜索框和底层页面间的阴影*/
  }
  .second {
    // box-sizing: border-box;
    // padding: 30px 350px 0 350px;
    width: 100%;
    position: relative;
    margin: 50px 0 50px 0;
    .searchbar {
      // position: absolute;
      // bottom: 10px;
      width: 100%;
      height: 80px;
      padding: 10px;
      box-sizing: border-box;
      .search{
        width:500px;
      }
    }
    .blank{
      height: 80px;
      padding: 10px;
    }
    .fix{
      position: fixed;
      background:black;
      top:0px;
      z-index: 1000;
      height:110px;
    }
    .checkbox-area {
      font-size: 50px;
      opacity: 0.9;
      margin-top:20px;
      color:white;
      /*  设置本区域里悬浮框底部的距离*/
    }
    .collapse-area {
      width: 1250px;
      margin-top: 100px;
      opacity: 0.8;
      /*  不透明度*/
    }
    .collapse-panel {
      margin-top: 10px;
      animation-name: fadeIn; /*动画名称*/
      animation-duration: 0.5s; /*动画持续时间*/
      animation-iteration-count: 1; /*动画次数*/
      animation-delay: 0s; /*延迟时间*/
    }
  }
  .third {
    .img-container {
      width: 1250px;
      // flex-wrap: wrap;
      margin-top: 30px;
      .img-item {
        margin:5px 0 5px 0;
        position: relative;
        height:275px;
        .image-slot {
          display: block;
          background-color: #fff;
          font-size: 50px;
          height:100%;
          line-height: 275px;
          color: aqua;
        }
        .img-hover-info {
          width: 100%;
          height: 100%;
          position: absolute;
          top: 0px;
          left: 0px;
          /*background:rgba(255, 165, 79, 0.5);*/
          text-align: left;
          color: #fff;
          word-wrap: break-word;
          word-break: normal;
          display: flex;
          align-items: left;
          /*justify-content: space-around;*/
          flex-direction: column;
          /*padding: 20px;*/
          box-sizing: border-box;
          background: rgba(90, 90, 90, 0.5);
          .title {
            width: 100%;
            text-align: center;
            font-size: 30px;
          }
          .desc {
            font-size: 10px;
          }
        }
      }
    }
  }
  .footer-btn {
    margin-top: 30px;
  }
}
.triangle {
  //width: 100%;
  /*margin-left: 10px;*/
  // height: 10px;
  line-height: 30px;
  font-size: 20px;
  // margin-top: 100px;
  /*"Select what you want"字体大小调节*/
  text-align: left;
  display: flex;
  align-items: center;
  cursor: pointer;
  .triangle-item {
    width: 0;
    height: 0;
    overflow: hidden;
    border-left: 10px solid #ffffff;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
    transition: transform 0.2s ease-in;
  }
}
/deep/.el-collapse-item__arrow {
  display: none !important;
}
.rotate {
  transform: rotate(90deg);
  transition: transform 0.2s ease-in;
}
@keyframes fadeIn {
  0% {
    opacity: 0; /*初始状态 透明度为0*/
  }
  50% {
    opacity: 0.5; /*中间状态 透明度为0*/
  }
  100% {
    opacity: 1; /*结尾状态 透明度为1*/
  }
}
.text-color {
  color: white;
  font-family: "cursive";
}
.fig {
  width: 100%;
  height: 100%;
}
  .logoText{
    font-family: cursive;
    font-size: 100px;
    color: white;
  }
  .logoText2{
  font-family: cursive;
  font-size: 50px;
  color: white;
}
/*
.fade-enter,
.fade-leave-active {
  opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
*/
</style>
<style lang="less">
.home {
  .el-image {
    display: unset;
  }
  .el-collapse-item__wrap {
    background-color: red;
  }
  .el-collapse-item__header {
    background-color: blue;
    border-bottom: 1px solid blue;
  }
  .loading {
    text-align: left;
    color: #409EFF;
    margin: 3px 0;
    font-size: 14px;
    .el-loading-mask {
      line-height: 30px;  
      .el-loading-spinner {
        text-align: left;
        font-size: 15px;
        .el-loading-text {
          display: inline-block;
          margin-left: 10px;
        }
      }
    }
  }
}
</style>