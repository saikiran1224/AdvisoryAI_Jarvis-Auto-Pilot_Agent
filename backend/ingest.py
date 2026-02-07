"""
Standalone Ingestion Script for Jarvis Auto-Pilot Agent
Run this to populate the ChromaDB vector database with client documents.
"""
import sys
import os
from pathlib import Path

# Ensure backend modules are importable
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir
sys.path.append(str(backend_dir))

try:
    from rag_system import ingest_documents, RAGSystem
except ImportError as e:
    print(f"❌ Error importing rag_system: {e}")
    sys.exit(1)

def run_ingestion():
    print("🚀 Jarvis Document Ingestion")
    print("==========================")
    
    # define paths
    docs_dir = current_dir / "data" / "client_documents"
    db_dir = current_dir / "data" / "chroma_db"
    
    print(f"📂 Looking for documents in: {docs_dir}")
    print(f"💾 Vector DB location: {db_dir}")
    
    # Ensure directories exist
    if not docs_dir.exists():
        print(f"❌ Directory not found: {docs_dir}")
        print("Creating it now...")
        docs_dir.mkdir(parents=True, exist_ok=True)
        print("Please add your .docx files to this folder and run again.")
        return

    # Check for files
    files = list(docs_dir.glob("*.docx"))
    if not files:
        print("⚠️ No .docx files found in the directory!")
        print(f"Please copy your client documents into: {docs_dir}")
        return

    print(f"📄 Found {len(files)} documents to ingest.")
    
    # Run ingestion with size check
    try:
        total_processed = 0
        total_skipped = 0
        
        # Override process to add size check (using internal method effectively)
        # Or better: filter files before passing to library if possible.
        # But library takes a directory. 
        # Let's iterate files manually and call ingest_document one by one
        
        rag = RAGSystem()
        
        for file_path in files:
            # Check size
            size_mb = file_path.stat().st_size / (1024 * 1024)
            if size_mb > 5.0:
                print(f"⚠️ Skipping large file ({size_mb:.1f}MB): {file_path.name}")
                total_skipped += 1
                continue
                
            print(f"Processing: {file_path.name}...")
            rag.ingest_document(str(file_path))
            total_processed += 1
            
        print("\n✅ Ingestion Complete!")
        print(f"   Processed {total_processed} files")
        print(f"   Skipped {total_skipped} large files")
        
        # Verify
        rag = RAGSystem()
        stats = rag.get_stats()
        print(f"\n📊 System Stats:")
        print(f"   Total Chunks in DB: {stats['total_chunks']}")
        
    except Exception as e:
        print(f"\n❌ Ingestion Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_ingestion()
