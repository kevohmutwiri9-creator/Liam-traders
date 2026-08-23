import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-20">
        <div className="container">
          <div className="max-w-3xl">
            <h1 className="text-5xl font-bold mb-6">
              Liam Traders
            </h1>
            <p className="text-xl mb-8 text-primary-100">
              Earn through legitimate work, learn valuable skills, and build your career. 
              Start with surveys and microtasks, advance to professional projects, and become an instructor.
            </p>
            <div className="flex gap-4">
              <Link href="/auth/register">
                <Button size="lg" className="bg-white text-primary-600 hover:bg-gray-100">
                  Get Started
                </Button>
              </Link>
              <Link href="/auth/login">
                <Button size="lg" variant="outline" className="border-white text-white hover:bg-white/10">
                  Sign In
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Level Progression */}
      <section className="py-16 bg-white">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">Level Progression System</h2>
          <div className="grid md:grid-cols-5 gap-6">
            {[
              { level: 1, name: "Starter", desc: "Surveys, simple tasks" },
              { level: 2, name: "Worker", desc: "Microtasks, data entry" },
              { level: 3, name: "Professional", desc: "Freelance work" },
              { level: 4, name: "Expert", desc: "Programming projects" },
              { level: 5, name: "Master", desc: "Instructor, mentor" },
            ].map((item) => (
              <Card key={item.level} className="text-center">
                <CardHeader>
                  <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-primary-100 flex items-center justify-center">
                    <span className="text-2xl font-bold text-primary-600">{item.level}</span>
                  </div>
                  <CardTitle>{item.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{item.desc}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-gray-50">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">Platform Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <Card>
              <CardHeader>
                <CardTitle>💰 Earn</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Complete surveys, microtasks, and freelance projects. Get paid for legitimate work.
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>📚 Learn</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Access programming courses, tutorials, and assessments. Develop skills for higher-paying work.
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>🎓 Teach</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Reach Level 5 to become an instructor. Create courses and mentor others.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Payment Methods */}
      <section className="py-16 bg-white">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">Payment Methods</h2>
          <div className="flex justify-center gap-8 flex-wrap">
            <Badge variant="secondary" className="text-lg px-6 py-3">M-Pesa</Badge>
            <Badge variant="secondary" className="text-lg px-6 py-3">Airtel Money</Badge>
            <Badge variant="secondary" className="text-lg px-6 py-3">Bank Transfer</Badge>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 bg-primary-600 text-white">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Start Earning?</h2>
          <p className="text-xl mb-8 text-primary-100">
            Join thousands of users already earning on Liam Traders
          </p>
          <Link href="/auth/register">
            <Button size="lg" className="bg-white text-primary-600 hover:bg-gray-100">
              Create Free Account
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="container text-center">
          <p className="text-gray-400">© 2026 Liam Traders. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
