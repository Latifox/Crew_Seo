"""
Content Analysis Tool

This tool analyzes content for SEO factors including keyword usage, readability,
content structure, and opportunities for improvement.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class ContentAnalysisInput(BaseModel):
    """Input schema for content analysis."""
    content: str = Field(..., description="The content to analyze")
    target_keywords: List[str] = Field(..., description="Target keywords to check for")
    min_word_count: Optional[int] = Field(
        default=300, 
        description="Minimum recommended word count"
    )


class ContentAnalysisTool(BaseTool):
    """Tool for analyzing content for SEO factors."""
    
    name: str = "Content Analysis Tool"
    description: str = """
    Analyze content for SEO optimization opportunities. This tool evaluates factors
    such as keyword usage, content structure, readability, and overall SEO score.
    It provides actionable recommendations for improving content quality and search
    engine visibility.
    """
    
    def __init__(self):
        """Initialize the Content Analysis Tool."""
        super().__init__()
    
    def _calculate_keyword_density(self, content: str, keyword: str) -> float:
        """
        Calculate keyword density for a specific keyword.
        
        Args:
            content: The content to analyze.
            keyword: The keyword to calculate density for.
            
        Returns:
            The keyword density as a percentage.
        """
        total_words = len(content.split())
        if total_words == 0:
            return 0.0
            
        # Count exact keyword occurrences (case insensitive)
        keyword_count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', content.lower()))
        
        return (keyword_count / total_words) * 100
    
    def _analyze_readability(self, content: str) -> Dict[str, Any]:
        """
        Analyze content readability.
        
        Args:
            content: The content to analyze.
            
        Returns:
            Readability metrics and assessment.
        """
        # Split content into sentences and words
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = content.split()
        total_words = len(words)
        total_sentences = len(sentences)
        
        if total_sentences == 0 or total_words == 0:
            return {
                "score": "Invalid",
                "average_words_per_sentence": 0,
                "assessment": "Unable to analyze empty content.",
                "recommendations": ["Add meaningful content to analyze."]
            }
        
        # Calculate average words per sentence
        avg_words_per_sentence = total_words / total_sentences
        
        # A very simple readability assessment based on sentence length
        # In a real implementation, we would use more sophisticated measures
        # like Flesch-Kincaid or SMOG Index
        if avg_words_per_sentence > 25:
            readability = "Difficult"
            assessment = "Content may be difficult to read due to long sentences."
            recommendations = ["Consider breaking longer sentences into shorter ones.", 
                              "Aim for an average of 15-20 words per sentence."]
        elif avg_words_per_sentence > 20:
            readability = "Moderate"
            assessment = "Content has reasonable readability but could be improved."
            recommendations = ["Some sentences could be shortened for better readability."]
        else:
            readability = "Good"
            assessment = "Content has good readability with appropriate sentence length."
            recommendations = ["Maintain this level of clarity throughout all content."]
        
        # Count paragraphs
        paragraphs = content.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        total_paragraphs = len(paragraphs)
        
        # Check paragraph length
        long_paragraphs = sum(1 for p in paragraphs if len(p.split()) > 100)
        if long_paragraphs > 0 and total_paragraphs > 0:
            if long_paragraphs / total_paragraphs > 0.3:
                recommendations.append("Consider breaking long paragraphs into smaller chunks.")
        
        return {
            "score": readability,
            "average_words_per_sentence": round(avg_words_per_sentence, 1),
            "sentences": total_sentences,
            "paragraphs": total_paragraphs,
            "assessment": assessment,
            "recommendations": recommendations
        }
    
    def _analyze_headings(self, content: str) -> Dict[str, Any]:
        """
        Analyze heading structure in the content.
        
        Args:
            content: The content to analyze.
            
        Returns:
            Heading structure analysis and recommendations.
        """
        # Find all markdown headings
        h1_pattern = r'^#\s+(.+)$'
        h2_pattern = r'^##\s+(.+)$'
        h3_pattern = r'^###\s+(.+)$'
        h4_pattern = r'^####\s+(.+)$'
        
        # Find headings using regex
        h1_headings = re.findall(h1_pattern, content, re.MULTILINE)
        h2_headings = re.findall(h2_pattern, content, re.MULTILINE)
        h3_headings = re.findall(h3_pattern, content, re.MULTILINE)
        h4_headings = re.findall(h4_pattern, content, re.MULTILINE)
        
        # Count of each heading type
        h1_count = len(h1_headings)
        h2_count = len(h2_headings)
        h3_count = len(h3_headings)
        h4_count = len(h4_headings)
        
        recommendations = []
        assessment = "Heading structure analysis:"
        
        # Analyze heading structure
        if h1_count == 0:
            recommendations.append("Add an H1 heading (main title) to your content.")
            assessment += " Missing H1 heading."
        elif h1_count > 1:
            recommendations.append("Use only one H1 heading per page for proper SEO.")
            assessment += " Multiple H1 headings detected."
        
        if h2_count == 0 and len(content) > 300:
            recommendations.append("Break content into sections using H2 headings.")
            assessment += " No section headings (H2) found."
        
        if h2_count > 0 and h3_count == 0 and len(content) > 1000:
            recommendations.append("Consider using H3 headings for subsections within major sections.")
        
        if h2_count > 7:
            recommendations.append("Consider consolidating some sections - too many H2 headings can dilute focus.")
        
        # Check heading hierarchy
        if h3_count > 0 and h2_count == 0:
            recommendations.append("Fix heading hierarchy: H3 headings should be used after H2 headings, not directly after H1.")
            assessment += " Improper heading hierarchy."
        
        if h4_count > 0 and h3_count == 0:
            recommendations.append("Fix heading hierarchy: H4 headings should be used after H3 headings.")
            assessment += " Improper heading hierarchy."
        
        if not recommendations:
            assessment = "Heading structure looks good."
            recommendations.append("Maintain consistent heading hierarchy for future content.")
        
        return {
            "h1_count": h1_count,
            "h2_count": h2_count,
            "h3_count": h3_count,
            "h4_count": h4_count,
            "assessment": assessment,
            "recommendations": recommendations
        }
    
    def _check_keyword_usage(
        self, 
        content: str, 
        target_keywords: List[str]
    ) -> Dict[str, Any]:
        """
        Check keyword usage in the content.
        
        Args:
            content: The content to analyze.
            target_keywords: List of target keywords to check for.
            
        Returns:
            Keyword usage analysis and recommendations.
        """
        content_lower = content.lower()
        results = {}
        all_recommendations = []
        overall_assessment = ""
        
        # Find headings
        heading_pattern = r'^#{1,4}\s+(.+)$'
        headings = re.findall(heading_pattern, content, re.MULTILINE)
        headings_text = " ".join(headings).lower()
        
        # First 100 words (approximate introduction)
        words = content.split()
        intro = " ".join(words[:min(100, len(words))]).lower()
        
        for keyword in target_keywords:
            keyword_lower = keyword.lower()
            
            # Check overall presence
            count = content_lower.count(keyword_lower)
            density = self._calculate_keyword_density(content, keyword)
            
            # Check presence in headings
            in_headings = keyword_lower in headings_text
            
            # Check presence in intro
            in_intro = keyword_lower in intro
            
            # Check presence in URL (simulated)
            in_url = False  # In a real tool, we would check the actual URL
            
            # Assess keyword usage
            keyword_recommendations = []
            
            if count == 0:
                assessment = "Missing"
                keyword_recommendations.append(f"Add the keyword '{keyword}' to your content.")
            elif count == 1:
                assessment = "Underused"
                keyword_recommendations.append(f"Use the keyword '{keyword}' more frequently throughout the content.")
            elif density > 3.0:
                assessment = "Overused (potential keyword stuffing)"
                keyword_recommendations.append(f"Reduce usage of '{keyword}' to avoid keyword stuffing.")
            elif density >= 0.5 and density <= 2.5:
                assessment = "Optimal"
            else:
                assessment = "Present"
            
            # Specific recommendations
            if not in_headings and count > 0:
                keyword_recommendations.append(f"Include '{keyword}' in at least one heading.")
            
            if not in_intro and count > 0:
                keyword_recommendations.append(f"Include '{keyword}' in the introduction section.")
            
            # Add to results
            results[keyword] = {
                "count": count,
                "density": round(density, 2),
                "in_headings": in_headings,
                "in_intro": in_intro,
                "in_url": in_url,
                "assessment": assessment,
                "recommendations": keyword_recommendations
            }
            
            # Add keyword-specific recommendations to overall list
            all_recommendations.extend(keyword_recommendations)
        
        # Overall assessment
        optimal_count = sum(1 for k, v in results.items() if v["assessment"] == "Optimal")
        missing_count = sum(1 for k, v in results.items() if v["assessment"] == "Missing")
        
        if missing_count == len(target_keywords):
            overall_assessment = "No target keywords found in content."
        elif optimal_count == len(target_keywords):
            overall_assessment = "All keywords are used optimally."
        else:
            overall_assessment = f"{optimal_count} of {len(target_keywords)} keywords used optimally."
        
        return {
            "keywords": results,
            "overall_assessment": overall_assessment,
            "recommendations": all_recommendations
        }
    
    def _analyze_content_completeness(self, content: str, min_word_count: int) -> Dict[str, Any]:
        """
        Analyze content completeness and structure.
        
        Args:
            content: The content to analyze.
            min_word_count: Minimum recommended word count.
            
        Returns:
            Content completeness analysis and recommendations.
        """
        word_count = len(content.split())
        
        # Check for key content components
        has_intro = False
        has_conclusion = False
        has_bullet_points = '•' in content or '*' in content or '-' in content
        
        paragraphs = content.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        if paragraphs and len(paragraphs[0].split()) >= 30:
            has_intro = True
        
        if paragraphs and len(paragraphs[-1].split()) >= 30:
            has_conclusion = True
        
        # Assess content completeness
        recommendations = []
        
        if word_count < min_word_count:
            recommendations.append(f"Increase content length to at least {min_word_count} words (currently {word_count}).")
        
        if not has_intro:
            recommendations.append("Add a proper introduction section (at least 30 words).")
        
        if not has_conclusion:
            recommendations.append("Add a proper conclusion section (at least 30 words).")
        
        if not has_bullet_points and word_count > 500:
            recommendations.append("Add bullet points or lists to break up long text sections.")
        
        # Check for call to action
        cta_phrases = ["learn more", "sign up", "get started", "contact us", "call now", "subscribe"]
        has_cta = any(phrase in content.lower() for phrase in cta_phrases)
        
        if not has_cta:
            recommendations.append("Add a clear call-to-action (CTA) to guide readers on next steps.")
        
        assessment = "Content structure assessment:"
        if not recommendations:
            assessment += " Content is well-structured and complete."
        else:
            assessment += f" Content needs improvement ({len(recommendations)} issues found)."
        
        return {
            "word_count": word_count,
            "has_intro": has_intro,
            "has_conclusion": has_conclusion,
            "has_bullet_points": has_bullet_points,
            "has_cta": has_cta,
            "assessment": assessment,
            "recommendations": recommendations
        }
    
    def _run(self, tool_input: str) -> str:
        """
        Execute the Content Analysis Tool.
        
        Args:
            tool_input: JSON string containing the tool input.
            
        Returns:
            Tool execution result as formatted markdown.
        """
        try:
            # Parse the tool input
            input_dict = json.loads(tool_input)
            
            content = input_dict.get("content", "")
            target_keywords = input_dict.get("target_keywords", [])
            min_word_count = input_dict.get("min_word_count", 300)
            
            if not content:
                return "Error: No content provided for analysis."
            
            if not target_keywords:
                return "Error: No target keywords provided for analysis."
                
            # Perform the analysis
            readability = self._analyze_readability(content)
            heading_analysis = self._analyze_headings(content)
            keyword_analysis = self._check_keyword_usage(content, target_keywords)
            completeness = self._analyze_content_completeness(content, min_word_count)
            
            # Calculate overall SEO score (simplified)
            # In a real implementation, this would be more sophisticated
            score_components = []
            
            # Readability score (0-25)
            if readability["score"] == "Good":
                score_components.append(25)
            elif readability["score"] == "Moderate":
                score_components.append(15)
            else:
                score_components.append(5)
            
            # Heading structure score (0-25)
            heading_score = 0
            if heading_analysis["h1_count"] == 1:
                heading_score += 10
            if heading_analysis["h2_count"] > 0:
                heading_score += 10
            if heading_analysis["h3_count"] > 0:
                heading_score += 5
            score_components.append(heading_score)
            
            # Keyword usage score (0-25)
            keyword_score = 0
            optimal_count = sum(1 for k, v in keyword_analysis["keywords"].items() if v["assessment"] == "Optimal")
            keyword_score = int((optimal_count / len(target_keywords)) * 25)
            score_components.append(keyword_score)
            
            # Content completeness score (0-25)
            completeness_score = 0
            if completeness["word_count"] >= min_word_count:
                completeness_score += 10
            if completeness["has_intro"]:
                completeness_score += 5
            if completeness["has_conclusion"]:
                completeness_score += 5
            if completeness["has_bullet_points"]:
                completeness_score += 3
            if completeness["has_cta"]:
                completeness_score += 2
            score_components.append(completeness_score)
            
            # Calculate total score
            total_score = sum(score_components)
            
            # Compile all recommendations
            all_recommendations = []
            all_recommendations.extend(readability["recommendations"])
            all_recommendations.extend(heading_analysis["recommendations"])
            all_recommendations.extend(keyword_analysis["recommendations"])
            all_recommendations.extend(completeness["recommendations"])
            
            # Format the result as markdown
            result = f"# Content Analysis Results\n\n"
            result += f"## Overall SEO Score: {total_score}/100\n\n"
            
            if total_score >= 90:
                result += "**Excellent!** Your content is very well optimized for SEO.\n\n"
            elif total_score >= 70:
                result += "**Good.** Your content is generally well optimized with some room for improvement.\n\n"
            elif total_score >= 50:
                result += "**Moderate.** Your content needs several improvements to be fully optimized.\n\n"
            else:
                result += "**Needs Work.** Your content requires significant optimization to perform well in search.\n\n"
            
            result += "## Content Overview\n\n"
            result += f"- **Word Count:** {completeness['word_count']} words"
            if completeness['word_count'] < min_word_count:
                result += f" (Recommended: {min_word_count}+ words)\n"
            else:
                result += "\n"
            result += f"- **Headings:** {heading_analysis['h1_count']} H1, {heading_analysis['h2_count']} H2, {heading_analysis['h3_count']} H3\n"
            result += f"- **Readability:** {readability['score']} ({readability['average_words_per_sentence']} words per sentence)\n"
            result += f"- **Target Keywords:** {len(target_keywords)}\n\n"
            
            result += "## Keyword Analysis\n\n"
            result += "| Keyword | Occurrences | Density | In Headings | In Intro | Assessment |\n"
            result += "|---------|------------|---------|-------------|----------|------------|\n"
            
            for keyword, analysis in keyword_analysis["keywords"].items():
                result += f"| {keyword} | {analysis['count']} | {analysis['density']}% | {'Yes' if analysis['in_headings'] else 'No'} | {'Yes' if analysis['in_intro'] else 'No'} | {analysis['assessment']} |\n"
            
            result += f"\n{keyword_analysis['overall_assessment']}\n\n"
            
            result += "## Top Recommendations\n\n"
            
            # Prioritize and deduplicate recommendations
            unique_recommendations = list(set(all_recommendations))
            for i, recommendation in enumerate(unique_recommendations[:10], 1):
                result += f"{i}. {recommendation}\n"
            
            if len(unique_recommendations) > 10:
                result += f"\n*Plus {len(unique_recommendations) - 10} more recommendations...*\n"
            
            return result
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON input."
        except Exception as e:
            return f"Error executing Content Analysis tool: {str(e)}"