;(function(root, factory, plugin) {
	
	factory(root.Zepto, plugin)
})(window, function($, plugin) {
	
	var __DEFAULTS__={
		autoLoop:false,
		loopTime:5000
	};
	var __PROTOTYPE__={
			init:function(){
				this.$carousel = $("#carousel");
				this.$inner = $("#carousel .inner");
				this.$lis = $("#carousel .inner li");
				this._vm = window.innerWidth;
				this.slide = this._vm *0.3;
				this.startX;
				this.endX;
				this.distX;
				this.cleft=-this._vm;
				this._dir;
				this.cindex = 0;
				this.total = this.$lis.length;
				
				this.$inner.css('transform','translate3d('+-this._vm+'px,0px,0px)')
				
			},
			_xlh:function(){
				this.$carousel.prepend("<ul id='indicators'></ul>");
				this.$indicators = $("#indicators");
				for(var i=0;i<this.total;i++){
					this.$indicators.append("<li></li>");
				};
				this.$indicate=this.$indicators.children("li");
				this.$indicate.eq(0).addClass("active");
			},
			_bind:function(){
				
				this.$carousel.on("touchstart", this.startcb.bind(this));
				this.$carousel.on("touchmove", this.movecb.bind(this));
				this.$carousel.on("touchend", this.endcb.bind(this));
				if(this.autoLoop){
					this.loop();
				}
			},
			startcb:function(e) {
				if(this.autoLoop){
					clearInterval(this.interval);
				}
				this.startX = e.touches[0].clientX;
//				console.log(this.$inner.css('transform').match(/\-[0-9]+/g))
//				if(this.$inner.css('transform').match(/\-[0-9]+/g)==null){
//					console.log(this.$inner.css('transform'))
//				}
//				this.cleft = parseFloat(this.$inner.css('transform').match(/\-[0-9]+/g)[0]);
				
				
				
			},
			movecb:function (e) {
				e.preventDefault();
				this.endX = e.touches[0].clientX;
				
				this.distX = this.startX - this.endX;
				
				this._dir = this.distX > 0 ? "L" : "R";

				this.$inner.css({
					'transform': 'translate3d('+(-this.distX+this.cleft)+'px,0px,0px)'
				});
			},
			endcb:function() {
				
				var abs = Math.abs(this.distX||0),
					_left;
					
				if(abs > this.slide) {
					
					if(this._dir == "L" ) {
						var x =-2*this._vm;

						this.$inner.animate({'transform':'translate3d('+x+'px,0px,0px)'},100,function(){
							this.cindex++;
						
						if(this.cindex==this.total){
							this.cindex =0;
						}

						this.$inner.children('li').eq(0).remove().clone(true).appendTo(this.$inner);
						this.$inner.css({'transform':'translate3d('+-this._vm+'px,0px,0px)'});
						this.$indicate.eq(this.cindex).addClass("active").siblings().removeClass("active");
						}.bind(this));
						
						
					} else if(this._dir == "R" ) {

						this.$inner.animate({'transform':'translate3d(0px,0px,0px)'},100,function(){
							this.cindex--;
						
						if(this.cindex<0){
							this.cindex =this.total-1;
						}
						

						this.$inner.children('li').eq(this.total-1).remove().clone(true).prependTo(this.$inner);
						this.$inner.css({'transform':'translate3d('+-this._vm+'px,0px,0px)'});
						this.$indicate.eq(this.cindex).addClass("active").siblings().removeClass("active");
						}.bind(this));
						
						
					}
				} else {
					
					this.$inner.animate({
						'transform': 'translate3d('+-this._vm+'px,0px,0px)'
					});

				}
				if(this.autoLoop){
					this.loop();
				}
			},
			loop:function(){
				this.interval = setInterval(function(){
						var date =new Date();
						var x =-2*this._vm;
						console.log(x)
						this.$inner.animate({'transform':'translate3d('+x+'px,0px,0px)'},100,function(){
							this.cindex++;
						if(this.cindex==this.total){
							this.cindex =0;
						}
						this.$inner.children('li').eq(0).remove().clone(true).appendTo(this.$inner);
						this.$inner.css({'transform':'translate3d('+-this._vm+'px,0px,0px)'});
						this.$indicate.eq(this.cindex).addClass("active").siblings().removeClass("active");
						}.bind(this));
						
						
					
					
				}.bind(this),this.loopTime);
			}
			
		}
	
	$.fn[plugin] = function(ops) {
		$.extend(this,__PROTOTYPE__,__DEFAULTS__,ops);
		
		this.init();
		this._xlh();
		this._bind();
	}
}, "myslider")