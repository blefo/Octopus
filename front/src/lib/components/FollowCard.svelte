<script>
    export let follow_content;
    export let onFollowQuestion = (question) => {};
    export let handleCustomQuestion = (question) => {};

    let search_question = "";
</script>

<div
    id={follow_content.groq_title}
    class="card carousel-item w-full rounded-box bg-base-100"
>
    <div class="card-body">
        <h2 class="card-title">{follow_content.groq_title}</h2>
        <div class="flex flex-row gap-2">
            {#each Object.entries(follow_content.sources) as [name, url]}
                <a href={url} target="_blank">
                    <div
                        class="badge text-white bg-[#ff7000] border-none p-2 gap-2"
                    >
                        <img
                            src={`https://www.google.com/s2/favicons?domain=${url}`}
                            alt={name}
                            class="w-4 h-4 rounded-full"
                        />
                        {name}
                    </div>
                </a>
            {/each}
        </div>
        <ul class="flex flex-col gap-2 pl-4 list-disc">
            <li>{follow_content.groq_key_point_1}</li>
            <li>{follow_content.groq_key_point_2}</li>
            <li>{follow_content.groq_key_point_3}</li>
        </ul>
        <h3 class="text-left mt-4 font-bold">Want to know more?</h3>
        <div class="flex flex-col gap-1 w-full">
            <button
                class="flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]"
                on:click={() =>
                    onFollowQuestion(follow_content.groq_question_1)}
            >
                {follow_content.groq_question_1}
                <p class="text-2xl text-[#ff7000] text-right">+</p>
            </button>
            <button
                class="flex border-t-2 pt-1 items-center flex-row text-left transition-all duration-300 hover:text-[#ff7000]"
                on:click={() =>
                    onFollowQuestion(follow_content.groq_question_2)}
            >
                {follow_content.groq_question_2}
                <p class="text-2xl text-right text-[#ff7000]">+</p>
            </button>
            <form
                class="flex border-t-2 border-b-[#ff7000] pb-2 pt-4"
                on:submit={(e) => {
                    e.preventDefault();
                    handleCustomQuestion(search_question);
                }}
            >
                <input
                    type="text"
                    placeholder="Have a question?"
                    class="w-full outline-none text-[#ff7000]"
                    bind:value={search_question}
                />
                <button type="submit" class="text-2xl text-[#ff7000]">+</button>
            </form>
        </div>
    </div>
</div>
