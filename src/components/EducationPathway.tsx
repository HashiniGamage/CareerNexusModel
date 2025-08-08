import React from 'react';
import { BookOpen, Award, Clock, DollarSign, MapPin, Users } from 'lucide-react';

interface PredictionData {
  jobTitle: string;
  currentDemand: number;
  predictedGrowth: number;
  confidenceScore: number;
  salaryRange: string;
  skillsRequired: string[];
}

interface EducationPathwayProps {
  predictions: PredictionData[];
  industry: string;
  experience: string;
}

interface EducationRecommendation {
  title: string;
  type: 'Degree' | 'Certification' | 'Bootcamp' | 'Online Course';
  institution: string;
  duration: string;
  cost: string;
  format: 'Online' | 'In-Person' | 'Hybrid';
  skillsGained: string[];
  careerAlignment: number;
  description: string;
}

const EducationPathway: React.FC<EducationPathwayProps> = ({ predictions, industry, experience }) => {
  const generateEducationRecommendations = (): EducationRecommendation[] => {
    const baseRecommendations: Record<string, EducationRecommendation[]> = {
      technology: [
        {
          title: 'BSc Computer Science',
          type: 'Degree',
          institution: 'University of Colombo',
          duration: '4 years',
          cost: 'LKR 800,000 - 1,200,000',
          format: 'In-Person',
          skillsGained: ['Programming', 'Algorithms', 'Database Design', 'Software Engineering'],
          careerAlignment: 95,
          description: 'Comprehensive computer science degree with strong industry connections.'
        },
        {
          title: 'AWS Cloud Practitioner',
          type: 'Certification',
          institution: 'Amazon Web Services',
          duration: '3-6 months',
          cost: 'LKR 50,000 - 100,000',
          format: 'Online',
          skillsGained: ['Cloud Computing', 'AWS Services', 'DevOps', 'Infrastructure'],
          careerAlignment: 88,
          description: 'Industry-recognized cloud certification for modern infrastructure skills.'
        },
        {
          title: 'Full Stack Web Development',
          type: 'Bootcamp',
          institution: 'SLIIT Academy',
          duration: '6-9 months',
          cost: 'LKR 150,000 - 250,000',
          format: 'Hybrid',
          skillsGained: ['React', 'Node.js', 'JavaScript', 'Database Management'],
          careerAlignment: 92,
          description: 'Intensive practical training for modern web development roles.'
        }
      ],
      healthcare: [
        {
          title: 'Healthcare Data Analytics',
          type: 'Certification',
          institution: 'University of Moratuwa',
          duration: '6-12 months',
          cost: 'LKR 120,000 - 200,000',
          format: 'Hybrid',
          skillsGained: ['Healthcare Analytics', 'Medical Data', 'Statistical Analysis', 'Compliance'],
          careerAlignment: 90,
          description: 'Specialized certification in healthcare data and analytics.'
        },
        {
          title: 'Digital Health Management',
          type: 'Online Course',
          institution: 'Harvard Medical School (Online)',
          duration: '4-6 months',
          cost: 'USD 2,000 - 3,500',
          format: 'Online',
          skillsGained: ['Digital Health', 'Telemedicine', 'Health Technology', 'Patient Care'],
          careerAlignment: 85,
          description: 'Leading-edge digital health management from global experts.'
        }
      ],
      finance: [
        {
          title: 'FinTech and Digital Banking',
          type: 'Certification',
          institution: 'Institute of Bankers Sri Lanka',
          duration: '6-9 months',
          cost: 'LKR 100,000 - 180,000',
          format: 'Hybrid',
          skillsGained: ['FinTech', 'Digital Banking', 'Blockchain', 'Financial Analytics'],
          careerAlignment: 93,
          description: 'Comprehensive fintech education tailored for Sri Lankan market.'
        },
        {
          title: 'CFA Charter',
          type: 'Certification',
          institution: 'CFA Institute',
          duration: '2-4 years',
          cost: 'USD 3,000 - 5,000',
          format: 'Online',
          skillsGained: ['Investment Analysis', 'Portfolio Management', 'Ethics', 'Financial Reporting'],
          careerAlignment: 96,
          description: 'Globally recognized finance qualification for investment professionals.'
        }
      ]
    };

    return baseRecommendations[industry] || baseRecommendations.technology;
  };

  const recommendations = generateEducationRecommendations();

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Degree': return 'text-blue-600 bg-blue-100';
      case 'Certification': return 'text-green-600 bg-green-100';
      case 'Bootcamp': return 'text-purple-600 bg-purple-100';
      case 'Online Course': return 'text-orange-600 bg-orange-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getFormatIcon = (format: string) => {
    switch (format) {
      case 'Online': return '💻';
      case 'In-Person': return '🏫';
      case 'Hybrid': return '🔄';
      default: return '📚';
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
      <div className="flex items-center space-x-3 mb-6">
        <div className="p-2 bg-green-100 rounded-lg">
          <BookOpen className="h-5 w-5 text-green-600" />
        </div>
        <h2 className="text-xl font-semibold text-gray-900">Education Pathway Recommendations</h2>
      </div>

      <div className="mb-6 p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-xl">
        <p className="text-sm text-gray-700">
          Curated education programs aligned with high-growth opportunities in <strong>{industry}</strong> 
          for <strong>{experience}</strong> level professionals.
        </p>
      </div>

      <div className="space-y-6">
        {recommendations.map((recommendation, index) => (
          <div key={index} className="border border-gray-200 rounded-xl p-6 hover:shadow-md transition-all duration-200">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="text-lg font-semibold text-gray-900">{recommendation.title}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(recommendation.type)}`}>
                    {recommendation.type}
                  </span>
                </div>
                
                <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                  <div className="flex items-center space-x-1">
                    <MapPin className="h-4 w-4" />
                    <span>{recommendation.institution}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Clock className="h-4 w-4" />
                    <span>{recommendation.duration}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <span>{getFormatIcon(recommendation.format)}</span>
                    <span>{recommendation.format}</span>
                  </div>
                </div>

                <p className="text-sm text-gray-700 mb-4">{recommendation.description}</p>
              </div>

              <div className="text-right ml-6">
                <div className="flex items-center space-x-1 text-green-600 mb-1">
                  <Award className="h-4 w-4" />
                  <span className="font-semibold">{recommendation.careerAlignment}%</span>
                </div>
                <p className="text-xs text-gray-500">Career alignment</p>
              </div>
            </div>

            {/* Cost Information */}
            <div className="flex items-center space-x-6 mb-4 p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-2">
                <DollarSign className="h-4 w-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">Investment:</span>
                <span className="text-sm text-gray-900">{recommendation.cost}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="h-4 w-4 text-gray-600" />
                <span className="text-sm text-gray-700">
                  {recommendation.format === 'Online' ? 'Self-paced' : 'Class-based'}
                </span>
              </div>
            </div>

            {/* Skills Gained */}
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Skills You'll Gain:</p>
              <div className="flex flex-wrap gap-2">
                {recommendation.skillsGained.map((skill, skillIndex) => (
                  <span 
                    key={skillIndex}
                    className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Career Alignment Bar */}
            <div>
              <div className="flex justify-between text-sm text-gray-600 mb-1">
                <span>Career Alignment with Market Demand</span>
                <span>{recommendation.careerAlignment}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full"
                  style={{ width: `${recommendation.careerAlignment}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Learning Path Timeline */}
      <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommended Learning Timeline</h3>
        <div className="space-y-3">
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
            <div>
              <p className="font-medium text-gray-900">Start with foundational skills (3-6 months)</p>
              <p className="text-sm text-gray-600">Build core competencies in your chosen field</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-purple-500 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
            <div>
              <p className="font-medium text-gray-900">Pursue specialized certification (6-12 months)</p>
              <p className="text-sm text-gray-600">Gain industry-recognized credentials</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-bold">3</div>
            <div>
              <p className="font-medium text-gray-900">Apply skills in real projects (Ongoing)</p>
              <p className="text-sm text-gray-600">Build portfolio and gain practical experience</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EducationPathway;