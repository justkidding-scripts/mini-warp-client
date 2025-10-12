#!/bin/bash
# Automated GitHub Push Script for Mini WARP Client
# Run this after creating the repository on GitHub

set -e

echo "🚀 Pushing Mini WARP Client to GitHub..."
echo "================================================"

# Check if we're in the right directory
if [[ ! -f "warp_suite_manager.py" ]]; then
    echo "❌ Error: Please run this script from the mini-warp-client directory"
    exit 1
fi

# Check if git is initialized
if [[ ! -d ".git" ]]; then
    echo "❌ Error: Git repository not initialized"
    exit 1
fi

# Show current status
echo "📊 Repository Status:"
git log --oneline -5
echo ""
git status --short
echo ""

# Push to GitHub
echo "📤 Pushing to GitHub (origin/main)..."
if git push -u origin main; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🔗 Repository URL: https://github.com/FoundationAgents/mini-warp-client"
    echo ""
    echo "🎯 Next Steps:"
    echo "  1. Visit your repository on GitHub"
    echo "  2. Verify all files are uploaded correctly"
    echo "  3. Consider adding repository topics/tags"
    echo "  4. Share with your PhD research community"
    echo ""
    echo "📚 Repository Features Uploaded:"
    echo "  ✅ Complete Mini WARP Client implementation"
    echo "  ✅ Event callback shutdown fix"
    echo "  ✅ GUI and CLI modes"
    echo "  ✅ Comprehensive documentation"
    echo "  ✅ Installation scripts"
    echo "  ✅ Test suite"
else
    echo ""
    echo "❌ Push failed. Common solutions:"
    echo "  1. Ensure the GitHub repository exists:"
    echo "     https://github.com/FoundationAgents/mini-warp-client"
    echo "  2. Check your GitHub authentication"
    echo "  3. Verify repository permissions"
    echo ""
    echo "📖 See GITHUB_SETUP.md for detailed instructions"
    exit 1
fi