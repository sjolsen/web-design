<?xml version="1.0"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:blog="http://sj-olsen.com/blog"
    xmlns="http://www.w3.org/1999/xhtml">
  <xsl:output
      method="html"
      encoding="UTF-8"
      doctype-system="about:legacy-compat"
      indent="yes"/>

  <xsl:template match="/blog:document">
    <html>
      <head>
        <meta charset="utf-8" />
        <title><xsl:value-of select="blog:title"/></title>
        <link rel="stylesheet" href="style.css" type="text/css" />
      </head>
      <body>
        <header>
          <h1 class="title"><xsl:value-of select="blog:title"/></h1>
          <hr class="title" />
          <h2 class="subtitle"><xsl:value-of select="blog:subtitle"/></h2>
        </header>
        <div class="main-content">
          <div class="body-copy">
            <xsl:apply-templates select="blog:section"/>
          </div>
        </div>
        <footer><xsl:value-of select="blog:copyright"/></footer>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="blog:section">
    <h2 class="section"><xsl:value-of select="blog:title"/></h2>
    <xsl:apply-templates select="blog:body"/>
  </xsl:template>

  <xsl:template match="blog:code-block">
    <div class="code">
      <xsl:if test="blog:header">
        <div class="code-header">
          <xsl:apply-templates select="blog:header"/>
        </div>
      </xsl:if>
      <div class="code-body">
        <pre><xsl:apply-templates select="blog:body"/></pre>
      </div>
    </div>
  </xsl:template>

  <xsl:template match="blog:code">
    <span class="code"><xsl:apply-templates/></span>
  </xsl:template>

  <xsl:template match="*[namespace-uri()='http://www.w3.org/1999/xhtml']">
    <xsl:element name="{local-name()}">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

</xsl:stylesheet>
