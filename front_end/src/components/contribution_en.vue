<script setup lang="ts">
</script>

<template>
    <a-typography class="text-left">
        <a-typography-title :level="1">Help Wanted</a-typography-title>
        <a-typography-paragraph class="space-y-[4px]">
            <div>
                Basically, I need 3 types of help:
            </div>
            <div class="flex flex-col space-y-[4px]">
                <a-typography-text strong>• Food</a-typography-text>
                <a-typography-text strong>• A Place to take shower and wash clothes</a-typography-text>
                <a-typography-text strong>• Server Fee</a-typography-text>
            </div>
        </a-typography-paragraph>

        <a-typography-title :level="2">Food</a-typography-title>
        <a-typography-paragraph class="space-y-[4px]">
            <div>
                Basically, I need 2 types of food:
            </div>
            <div class="flex flex-col space-y-[4px]">
                <a-typography-text strong>• Instant Noodles</a-typography-text>
                <a-typography-text strong>• Shaqima</a-typography-text>
                <a-typography-text mark>You could contact me for package-receiving address, so that you could buy me some
                    food.</a-typography-text>
            </div>
        </a-typography-paragraph>

        <a-typography-title :level="2">A Place to take shower and wash clothes</a-typography-title>
        <a-typography-paragraph>
            You can invite me to a place to do those activities for free.
        </a-typography-paragraph>
        <a-typography-paragraph>
            Or you can send me 70 RMB so that I could do it by spend money.
        </a-typography-paragraph>

        <a-typography-title :level="2">Server Fee</a-typography-title>
        <a-typography-paragraph>
            For this server, it requires 5 dollars per month.
        </a-typography-paragraph>
        <a-typography-paragraph>
            You could send me money, after I deposit it to server provider, I could send you a screenshot as an deposition
            evidence.
        </a-typography-paragraph>

        <a-typography-title :level="2">My Wallet and Email</a-typography-title>
        <a-typography-paragraph>
            <div class="flex flex-col space-y-[4px]">
                <a-typography-link href="https://paypal.me/yingshaoxo" target="_blank">
                    Paypal: https://paypal.me/yingshaoxo
                </a-typography-link>
                <a-typography-link href="mailto: yingshaoxo@gmail.com" target="_blank">
                    Email: yingshaoxo@gmail.com
                </a-typography-link>
                <a-typography-text type="secondary">
                    > I also provide "Software Construction(CTO)" consultation service.
                </a-typography-text>
            </div>
        </a-typography-paragraph>
    </a-typography></template>