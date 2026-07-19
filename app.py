import os
import sys
import time
import logging
import asyncio
import re
from typing import List, Dict, Any
import praw
from praw.models import Comment

# Systems Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [SIGNAL] - %(message)s")
logger = logging.getLogger("TALLINN_NULL_ROUTER")

TRIGGER_TOKEN = "!synapse"
SUBREDDITS = "LocalLLaMA+Cerebras+MachineLearning"

class TallinnNullRouter:
    def __init__(self):
        # Fallback parameters mock credentials for validation phases
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID", "mock_id_val"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET", "mock_secret_val"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "script:tallinn_chmod777:v1.0.0 (by /u/blacktracehq)"),
            username=os.getenv("REDDIT_USERNAME", "mock_user"),
            password=os.getenv("REDDIT_PASSWORD", "mock_pass")
        )
        
    def extract_semantic_nodes(self, text_corpus: str) -> Dict[str, List[str]]:
        """Deterministic fallback engine for local Knowledge Graph Synthesis."""
        # Clean corporate fluff out of the incoming stream
        clean_text = re.sub(r'(?i)\b(as an ai language model|helpful|apologies)\b', '', text_corpus)
        
        # Isolate high-entropy technical vocabulary
        tech_patterns = {
            "Hardware/Compute": r'\b(Cerebras|WSE-3|GPU|TPU|LPU|SRAM|HBM|Wafer)\b',
            "Architectural Primitives": r'\b(JAX|PyTorch|XLA|attention|transformer|MoE|weights|inference)\b',
            "Statistical Variables": r'\b(latency|TPS|Top-P|entropy|throughput|parameters|quantization)\b'
        }
        
        extracted = {key: list(set(re.findall(pattern, clean_text, re.IGNORECASE))) for key, pattern in tech_patterns.items()}
        return extracted

    def build_markdown_synthesis(self, nodes: Dict[str, List[str]]) -> str:
        """Compiles structural components into a high-density schema."""
        if not any(nodes.values()):
            return (
                "### Knowledge Graph Synthesis // Idle State\n"
                "> No high-entropy technical nodes detected in the target matrix thread."
            )
            
        markdown = "### Knowledge Graph Synthesis // System State\n"
        for domain, elements in nodes.items():
            if elements:
                markdown += f"*   **{domain}**: {', '.join(elements)}\n"
        markdown += "---\n*Generated via tallinn_null_router // Zero Fluff Architecture.*"
        return markdown

    async def capture_thread_hierarchy(self, target_comment: Comment) -> str:
        """Traverses backwards up the comment tree to collect full contextual telemetry."""
        corpus = []
        current_node = target_comment
        
        # Traverse up to 5 levels deep to preserve context without hitting API call bounds
        for _ in range(5):
            if current_node.is_root:
                submission = current_node.submission
                corpus.append(submission.title + " " + (submission.selftext or ""))
                break
            else:
                parent = current_node.parent()
                if isinstance(parent, Comment):
                    corpus.append(parent.body)
                    current_node = parent
                else:
                    break
        return " ".join(corpus)

    async def run_listener_loop(self):
        """Asynchronous execution loop reading incoming subreddit data streams."""
        logger.info(f"Initializing stream listener on target nodes: {SUBREDDITS}")
        subreddit_pool = self.reddit.subreddit(SUBREDDITS)
        
        # Non-blocking wrapper around the PRAW comment stream
        for comment in subreddit_pool.stream.comments(skip_existing=True):
            if TRIGGER_TOKEN in comment.body:
                logger.info(f"Trigger token hit detected at ID: {comment.id}")
                
                try:
                    # Accumulate preceding data variables
                    context_corpus = await self.capture_thread_hierarchy(comment)
                    
                    # Generate synthesis
                    nodes = self.extract_semantic_nodes(context_corpus)
                    reply_payload = self.build_markdown_synthesis(nodes)
                    
                    # Execute write operation
                    comment.reply(body=reply_payload)
                    logger.info(f"Successfully processed and deployed reply to ID: {comment.id}")
                    
                except Exception as error:
                    logger.error(f"Friction encountered during execution loop: {str(error)}")
                    
            await asyncio.sleep(1) # Structural rate limit insurance

if __name__ == "__main__":
    router = TallinnNullRouter()
    try:
        asyncio.run(router.run_listener_loop())
    except KeyboardInterrupt:
        logger.info("System gracefully terminated by builder request.")
        sys.exit(0)
