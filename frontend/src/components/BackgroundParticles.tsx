import React, { useEffect, useRef } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import './BackgroundParticles.css';

interface Particle {
  x: number;
  y: number;
  size: number;
  speedX: number;
  speedY: number;
  opacity: number;
  color: string;
}

const BackgroundParticles: React.FC = () => {
  const { theme } = useTheme();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<Particle[]>([]);
  const animationRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    const getThemeColors = () => {
      if (theme === 'dark') {
        return [
          '#60a5fa', // primary-400
          '#a78bfa', // secondary-400
          '#34d399', // emerald-400
          '#fbbf24', // yellow-400
          '#f472b6', // pink-400
        ];
      } else {
        return [
          '#3b82f6', // primary-500
          '#8b5cf6', // secondary-500
          '#10b981', // emerald-500
          '#f59e0b', // yellow-500
          '#ec4899', // pink-500
        ];
      }
    };

    const createParticle = (): Particle => {
      const colors = getThemeColors();
      return {
        x: Math.random() * canvas.width,
        y: canvas.height + 10,
        size: Math.random() * 3 + 1,
        speedX: (Math.random() - 0.5) * 2,
        speedY: -(Math.random() * 3 + 1),
        opacity: Math.random() * 0.6 + 0.2,
        color: colors[Math.floor(Math.random() * colors.length)],
      };
    };

    const initParticles = () => {
      particlesRef.current = [];
      for (let i = 0; i < 50; i++) {
        const particle = createParticle();
        particle.y = Math.random() * canvas.height;
        particlesRef.current.push(particle);
      }
    };

    const updateParticles = () => {
      const particles = particlesRef.current;
      
      for (let i = particles.length - 1; i >= 0; i--) {
        const particle = particles[i];
        
        particle.x += particle.speedX;
        particle.y += particle.speedY;
        
        // Fade out as they move up
        if (particle.y < canvas.height / 2) {
          particle.opacity -= 0.002;
        }
        
        // Remove particles that are off screen or fully transparent
        if (particle.y < -10 || particle.opacity <= 0) {
          particles.splice(i, 1);
        }
      }
      
      // Add new particles
      if (Math.random() < 0.3) {
        particles.push(createParticle());
      }
      
      // Limit particle count
      if (particles.length > 100) {
        particles.splice(0, particles.length - 100);
      }
    };

    const drawParticles = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      particlesRef.current.forEach(particle => {
        ctx.globalAlpha = particle.opacity;
        ctx.fillStyle = particle.color;
        
        // Add glow effect
        ctx.shadowColor = particle.color;
        ctx.shadowBlur = theme === 'dark' ? 10 : 5;
        
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.shadowBlur = 0;
      });
      
      ctx.globalAlpha = 1;
    };

    const animate = () => {
      updateParticles();
      drawParticles();
      animationRef.current = requestAnimationFrame(animate);
    };

    resizeCanvas();
    initParticles();
    animate();

    const handleResize = () => {
      resizeCanvas();
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [theme]);

  return (
    <canvas
      ref={canvasRef}
      className="background-particles-canvas"
    />
  );
};

export default BackgroundParticles;