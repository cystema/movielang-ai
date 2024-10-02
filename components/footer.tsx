import React from 'react'

import { cn } from '@/lib/utils'
import { ExternalLink } from '@/components/external-link'

export function FooterText({ className, ...props }: React.ComponentProps<'p'>) {
  return (
    <p
      className={cn(
        'px-2 text-center text-xs leading-normal',
        className
      )}
      {...props}
    >
      AI chatbot built with Langchain, Langflow, AstraDB, and Vercel AI SDK. Developed by {' '}
      <ExternalLink href="https://shubh.ink">Shubham</ExternalLink>.
    </p>
  )
}
