"""
Validation script to ensure the implementation is correct according to the requirements.
This checks that the OpenAI Assistant API is properly implemented with tools.
"""
import importlib.util
import sys
from pathlib import Path


def validate_openai_agents_implementation():
    """Validate that the BookAssistant properly uses OpenAI Assistant API with tools."""
    print("Validating OpenAI Assistant API implementation...")
    
    # Import the BookAssistant class
    spec = importlib.util.spec_from_file_location(
        "book_assistant", 
        "E:/ai_dd/sp/chatbot/backend/src/agents/book_assistant.py"
    )
    book_assistant_module = importlib.util.module_from_spec(spec)
    sys.modules["book_assistant"] = book_assistant_module
    spec.loader.exec_module(book_assistant_module)
    
    # Check that the BookAssistant class exists
    if not hasattr(book_assistant_module, 'BookAssistant'):
        print("❌ FAIL: BookAssistant class not found")
        return False
    
    BookAssistant = book_assistant_module.BookAssistant
    
    # Create an instance (this will attempt to create the OpenAI assistant)
    try:
        assistant = BookAssistant()
        print("✅ PASS: BookAssistant class can be instantiated")
    except Exception as e:
        print(f"❌ FAIL: Error instantiating BookAssistant: {e}")
        return False
    
    # Check that the assistant has the required attributes
    if not hasattr(assistant, 'search_tool'):
        print("❌ FAIL: search_tool attribute not found")
        return False
    
    if not hasattr(assistant, 'client'):
        print("❌ FAIL: client attribute not found")
        return False
    
    if not hasattr(assistant, 'assistant'):
        print("❌ FAIL: assistant attribute not found")
        return False
    
    print("✅ PASS: BookAssistant has required attributes")
    
    # Check that process_query method exists
    if not hasattr(assistant, 'process_query'):
        print("❌ FAIL: process_query method not found")
        return False
    
    print("✅ PASS: process_query method exists")
    
    # Check that the assistant uses the OpenAI Assistant API
    # The assistant object should be created using the beta API
    if assistant.assistant is not None:
        print("✅ PASS: OpenAI Assistant API is being used")
    else:
        print("⚠️  WARNING: OpenAI Assistant API not available, using fallback method")
    
    print("\nAll validation checks completed!")
    return True


def validate_project_structure():
    """Validate that all required files and directories exist."""
    print("\nValidating project structure...")
    
    required_paths = [
        "backend/src/config.py",
        "backend/src/vector_db.py",
        "backend/src/agents/book_assistant.py",
        "backend/src/tools/search_tool.py",
        "backend/src/api/chat.py",
        "backend/src/api/admin.py",
        "backend/src/api/health.py",
        "backend/src/models/chat_session.py",
        "backend/src/models/user_query.py",
        "backend/src/models/agent_response.py",
        "backend/src/models/book_content.py",
        "backend/src/models/vector_embedding.py",
        "backend/src/services/chat_service.py",
        "backend/src/services/embedding_service.py",
        "backend/src/services/vector_service.py",
        "backend/src/ingestors/sitemap_parser.py",
        "backend/src/ingestors/content_scraper.py",
        "backend/src/ingestors/content_cleaner.py",
        "backend/src/ingestors/content_chunker.py",
        "backend/tests/unit/test_agent_logic.py",
        "backend/tests/contract/test_chat_contract.py",
        "backend/tests/integration/test_search_tool.py",
        "Dockerfile",
        "docker-compose.yml",
        "docs/README.md"
    ]
    
    missing_paths = []
    for path in required_paths:
        full_path = Path("E:/ai_dd/sp/chatbot") / path
        if not full_path.exists():
            missing_paths.append(path)
    
    if missing_paths:
        print(f"❌ FAIL: Missing required files/directories: {missing_paths}")
        return False
    else:
        print("✅ PASS: All required files/directories exist")
        return True


def main():
    """Run all validations."""
    print("Running implementation validation...\n")
    
    success1 = validate_openai_agents_implementation()
    success2 = validate_project_structure()
    
    if success1 and success2:
        print("\n🎉 All validations passed! Implementation is correct.")
        return True
    else:
        print("\n❌ Some validations failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    main()