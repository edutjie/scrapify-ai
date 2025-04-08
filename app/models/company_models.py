from pydantic import BaseModel, Field


class CompanyScrapeRequest(BaseModel):
    linkedin_url: str = Field(..., description="LinkedIn company URL to scrape")


class CompanyProfile(BaseModel):
    name: str = Field(..., description="Company name")
    linkedin_internal_id: str = Field(..., description="LinkedIn internal ID")
    website: str = Field(..., description="Company website")
    industry: str = Field(..., description="Company industry")
    company_size: str = Field(..., description="Company size")
    company_size_on_linkedin: int = Field(..., description="Company size on LinkedIn")
    hq_location: str = Field(..., description="Headquarters location")
    company_type: str = Field(..., description="Company type")
    founded_year: int = Field(..., description="Year company was founded")
    tagline: str = Field(..., description="Company tagline")


class CompanyScrapeResponse(BaseModel):
    response: CompanyProfile = Field(
        ..., description="The scraped company profile data"
    )
