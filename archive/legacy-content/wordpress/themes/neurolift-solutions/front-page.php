<?php
/**
 * Template for the homepage
 *
 * @package NeuroLift_Solutions
 */

get_header();
?>

<main id="primary" class="site-main">
    
    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <h1><?php echo get_bloginfo('name'); ?></h1>
            <p style="font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">
                Human and AI Solidarity Without Singularity
            </p>
            <p><?php echo get_bloginfo('description'); ?></p>
            <div class="hero-buttons">
                <a href="#about" class="btn btn-primary">Learn More</a>
                <a href="/contact" class="btn btn-secondary">Get Started</a>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="content-section">
        <div class="container">
            <h2 class="section-title">About NeuroLift Technologies</h2>
            <div class="about-content">
                <p>
                    NeuroLift Technologies is pioneering AI-powered solutions for neurodivergent communities
                    and intelligent business operations through experiential learning and agent-based systems.
                </p>
            </div>

            <div class="card-grid">
                <div class="card">
                    <h3 class="card-title">AI Experiential Learning</h3>
                    <p>
                        Revolutionary Avatar-Aide-Advocate system where AI learns through authentic 
                        ADHD experiences and expert coaching.
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">TOI-OTOI Framework</h3>
                    <p style="font-weight: 600; color: var(--primary-color); margin-bottom: 0.5rem;">
                        "Human and AI Solidarity Without Singularity"
                    </p>
                    <p>
                        AI that respects your sovereignty instead of mining your data. Privacy-preserving 
                        framework ensuring user preferences and human control remain paramount.
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">Agent-Based Business</h3>
                    <p>
                        Complete AI agent ecosystem enabling two-person teams to orchestrate
                        billion-dollar operations.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="content-section">
        <div class="container">
            <h2 class="section-title">Our Innovation</h2>
            <div class="card-grid">
                <div class="card">
                    <h3 class="card-title">🎯 Avatar System</h3>
                    <p>
                        AI Avatars that embody specific ADHD traits and experience authentic 
                        struggles through realistic simulation scenarios.
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">🤝 Aide Coaching</h3>
                    <p>
                        Expert AI Aides combining PhD-level research with real-world community 
                        wisdom to provide effective coaching.
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">💡 Advocate Fusion</h3>
                    <p>
                        Fusion of Avatar experiences with Aide expertise creating advocates that 
                        both understand and solve ADHD challenges.
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">🔒 Privacy First</h3>
                    <p>
                        All processing happens locally with no data collection or external 
                        transmission without explicit consent.
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">🚀 Cloudflare Integration</h3>
                    <p>
                        Enterprise-grade hosting with Workers for edge computing, optimized 
                        caching, and global CDN delivery.
                    </p>
                </div>
                <div class="card">
                    <h3 class="card-title">🎮 Realistic Simulation</h3>
                    <p>
                        Sims/RPG-style environment with workplace, personal, social, and 
                        academic scenarios for comprehensive training.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- Founder's Vision Section -->
    <section class="content-section">
        <div class="container-narrow">
            <h2 class="section-title">Our Mission</h2>
            <blockquote style="font-size: 1.5rem; font-style: italic; text-align: center; color: var(--primary-color); margin-bottom: 2rem;">
                "Nothing About Us Without Us"
            </blockquote>
            <div style="background: var(--light-color); padding: 2rem; border-radius: 8px; margin-bottom: 2rem;">
                <h3 style="text-align: center; color: var(--dark-color); margin-bottom: 1rem;">A Message from Our Founder</h3>
                <p style="text-align: center; font-style: italic; margin-bottom: 1rem;">
                    I am <strong>Joshua Dorsey</strong>, Founder of NeuroLift Technologies. I am a visionary systems 
                    thinker, an ethical innovator, and—most importantly—<strong>I am neurodivergent</strong>.
                </p>
                <p style="text-align: center;">
                    I built NeuroLift because I was tired of tools designed to "fix" me. Living with ADHD gave me 
                    a front-row seat to the challenges of executive function, time blindness, and the overwhelming 
                    noise of the modern world. I didn't want an AI that acted like a nagging parent; I wanted a 
                    <strong>partner that understood my mental cycles</strong>.
                </p>
                <p style="text-align: center;">
                    NLT is my answer to a simple question: <strong>What if AI respected our sovereignty instead of 
                    mining our data?</strong>
                </p>
                <p style="text-align: center;">
                    This platform isn't just code; it's a <strong>digital ecosystem designed to elevate the 
                    neurodivergent mind</strong>, protecting your privacy and your dignity every step of the way.
                </p>
            </div>
            <p style="text-align: center; font-weight: 600; color: var(--primary-color);">
                We operate on the principle of "Nothing About Us, Without Us." Neurodivergent voices lead our 
                development. We're building AI that learns through authentic experience, creating systems that 
                truly understand what ADHD struggles feel like and what actually works.
            </p>
        </div>
    </section>

    <!-- Technology Stack -->
    <section class="content-section">
        <div class="container">
            <h2 class="section-title">Technology Stack</h2>
            <div class="card-grid">
                <div class="card">
                    <h3 class="card-title">Infrastructure</h3>
                    <ul>
                        <li>Cloudflare Workers & Pages</li>
                        <li>Supabase Database</li>
                        <li>Python Backend</li>
                        <li>WordPress CMS</li>
                    </ul>
                </div>
                <div class="card">
                    <h3 class="card-title">AI & Simulation</h3>
                    <ul>
                        <li>Avatar-Aide Architecture</li>
                        <li>TOI-OTOI Framework</li>
                        <li>Experiential Learning Engine</li>
                        <li>Behavioral Simulation</li>
                    </ul>
                </div>
                <div class="card">
                    <h3 class="card-title">Security & Performance</h3>
                    <ul>
                        <li>DDoS Protection</li>
                        <li>SSL/TLS Encryption</li>
                        <li>Edge Caching</li>
                        <li>CDN Global Delivery</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section class="content-section">
        <div class="container-narrow text-center">
            <h2 class="section-title">Get In Touch</h2>
            <p>
                Interested in learning more about NeuroLift Technologies? 
                We'd love to hear from you.
            </p>
            <div class="mt-2">
                <a href="mailto:neuro.edge24@gmail.com" class="btn btn-primary">Contact Us</a>
                <a href="/about" class="btn btn-secondary">Learn More</a>
            </div>
        </div>
    </section>

</main>

<?php
get_footer();
