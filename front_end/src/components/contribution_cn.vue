<script setup lang="ts">
import aili_pay from '../assets/aili_pay.jpeg'
import wechat_pay from '../assets/wechat_pay.png'
</script>

<template>
    <a-typography class="text-left">
        <a-typography-title :level="1">请求救助</a-typography-title>
        <a-typography-paragraph class="space-y-[4px]">
            <div>
                基本上，我需要2种类型的救助：
            </div>
            <div class="flex flex-col space-y-[4px]">
                <a-typography-text strong>• 食物</a-typography-text>
                <a-typography-text strong>• 一个可以免费洗澡、洗衣服的地方</a-typography-text>
                <!-- <a-typography-text strong>• 服务器费用</a-typography-text> -->
            </div>
        </a-typography-paragraph>

        <a-typography-title :level="2">食物</a-typography-title>
        <a-typography-paragraph class="space-y-[4px]">
            <div>
                基本上，我需要2种类型的食物：
            </div>
            <div class="flex flex-col space-y-[4px]">
                <a-typography-text strong>• 方便面</a-typography-text>
                <a-typography-text strong>• 沙琪玛</a-typography-text>
                <a-typography-text mark>你可以问我要收货地址，然后再从网上买给我。</a-typography-text>
            </div>
        </a-typography-paragraph>

        <a-typography-title :level="2">一个可以免费洗澡、洗衣服的地方</a-typography-title>
        <a-typography-paragraph>
            你可以邀请我去你们那儿免费洗澡、洗衣服。
        </a-typography-paragraph>
        <a-typography-paragraph>
            或者你也可以给我发70元红包，我去 自助洗衣、洗澡房 洗。
        </a-typography-paragraph>

        <!-- <a-typography-title :level="2">服务器费用</a-typography-title>
        <a-typography-paragraph>
          对于这个服务器，它需要5美元一个月。
        </a-typography-paragraph>
        <a-typography-paragraph>
          你可以给我打钱，然后我再存到服务器供应商，并且我可以给你提供充值截图。
        </a-typography-paragraph> -->

        <a-typography-title :level="2">我的邮箱与收款地址</a-typography-title>
        <a-typography-paragraph>
            <div class="flex flex-col space-y-[32px]">
                <div>
                    <a-typography-title :level="4">邮箱</a-typography-title>
                    <a-typography-link href="mailto: yingshaoxo@gmail.com" target="_blank">
                        yingshaoxo@gmail.com
                    </a-typography-link>
                </div>

                <div>
                    <a-typography-title :level="4">微信</a-typography-title>
                    <a-image :width="250" :src="wechat_pay" />
                </div>

                <div>
                    <a-typography-title :level="4">支付宝</a-typography-title>
                    <a-image :width="250" :src="aili_pay" />
                </div>
            </div>
        </a-typography-paragraph>

        <a-typography-title :level="2">顺便说一句</a-typography-title>
        <a-typography-paragraph>
            你要是不嫌麻烦，还可以在线下找我。
        </a-typography-paragraph>
        <a-typography-paragraph>
            没准我就住在你家附近。
        </a-typography-paragraph>
        <a-typography-text type="secondary">
            我还能提供 软件构架(CTO) 咨询服务
        </a-typography-text>
    </a-typography>
</template>