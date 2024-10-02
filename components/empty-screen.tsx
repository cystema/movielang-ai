import { UseChatHelpers } from 'ai/react'

import { Button } from '@/components/ui/button'
import { ExternalLink } from '@/components/external-link'
import { IconArrowRight } from '@/components/ui/icons'

export function EmptyScreen() {
  return (
    <div className="mx-auto max-w-2xl px-4">
      <div className="flex flex-col gap-2 rounded-lg border bg-background p-8">
        <h1 className="text-lg font-semibold">
          Welcome to MovieLang AI Chatbot!
        </h1>
        <p className="leading-normal text-muted-foreground">
          This is an AI chatbot built with{' '}
          <ExternalLink href="https://python.langchain.com/docs/introduction/">Langchain</ExternalLink>,{' '}
          <ExternalLink href="https://docs.langflow.org/">Langflow</ExternalLink>,{' '}
          <ExternalLink href="https://docs.datastax.com/en/astra-db-serverless/index.html">AstraDB</ExternalLink>,{' '}
          RAG,
          <ExternalLink href="https://nextjs.org">Next.js</ExternalLink>, and the{' '}
          <ExternalLink href="https://sdk.vercel.ai">
            Vercel AI SDK
          </ExternalLink>


          .
        </p>
        <p className="leading-normal text-muted-foreground">
          It leverages AstraDB’s Vector Database to store and retrieve movie data from the TMDB API, using advanced vector search to identify the most relevant movies based on user input. By combining Vector Search with Retrieval-Augmented Generation (RAG) and a Large Language Model (LLM), the chatbot generates intelligent, context-aware responses for an enhanced user experience.
        </p>
      </div>
    </div>
  )
}
