import ReactMarkdown from "react-markdown";

export function Markdown({ children }: { children: any }) {
    return (
        <ReactMarkdown
            components={{
                ol: ({ children }) => (
                    <ol className="p-4 list-inside grid gap-4">{children}</ol>
                ),
                ul: ({ children }) => (
                    <ul className="p-2 list-inside grid gap-4">{children}</ul>
                ),
            }}
        >
            {children}
        </ReactMarkdown>
    );
}
