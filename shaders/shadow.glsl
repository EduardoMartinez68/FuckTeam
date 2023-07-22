// Vertex shader
#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 lightSpaceMatrix;

out vec4 fragPosition;
out vec4 shadowCoord;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
    fragPosition = model * vec4(position, 1.0);
    shadowCoord = lightSpaceMatrix * fragPosition;
}

// Fragment shader
#version 330 core

in vec4 fragPosition;
in vec4 shadowCoord;

uniform sampler2D shadowMap;

out vec4 fragColor;

float ShadowCalculation(vec4 fragPosLightSpace)
{
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    projCoords = projCoords * 0.5 + 0.5;
    
    float closestDepth = texture(shadowMap, projCoords.xy).r;
    float currentDepth = projCoords.z;
    
    float shadow = (currentDepth > closestDepth + 0.005) ? 1.0 : 0.0;
    
    return shadow;
}

void main()
{
    vec3 lightColor = vec3(1.0, 1.0, 1.0);
    vec3 objectColor = vec3(0.5, 0.5, 0.5);
    
    vec4 fragPosLightSpace = shadowCoord;
    float shadow = ShadowCalculation(fragPosLightSpace);
    
    vec3 lighting = lightColor * (1.0 - shadow);
    fragColor = vec4(objectColor * lighting, 1.0);
}
