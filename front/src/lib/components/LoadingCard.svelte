<script>
    // fade in transition
    import { fade } from "svelte/transition";
    export let question = "Loading...";
</script>

<div
    id="loading-card"
    in:fade={{ duration: 2000 }}
    class="card carousel-item w-full rounded-box bg-base-100"
>
    <div class="card-body">
        <h2 class="card-title">{question}</h2>
        <div class="flex flex-row gap-2">
            <div class="badge skeleton bg-[#ff7000]/40 w-12 text-white p-2 gap-2"></div>
            <div class="badge skeleton bg-[#ff7000]/40 w-12 text-white p-2 gap-2"></div>
        </div>
        <ul class="flex flex-col gap-2 pl-4 list-disc">
            <li class="skeleton h-12"></li>
            <li class="skeleton h-12"></li>
            <li class="skeleton h-12"></li>
        </ul>
        <h3 class="text-left mt-4 font-bold">Want to know more?</h3>
        <div class="flex flex-col gap-2 w-full">
            <button
                class="skeleton h-6 flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]"
            >
            </button>
            <button
                class="skeleton h-6 flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]"
            >
            </button>
            <button
                class="skeleton h-6 flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]"
            >
            </button>
            <div class="flex border-t-2 border-b-[#ff7000] pb-2 pt-4">
                <p
                    type="text"
                    placeholder="Have a question?"
                    class="skeleton h-6 w-full outline-none text-[#ff7000]"
                />
            </div>
        </div>
    </div>
</div>
